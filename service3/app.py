from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
import pandas as pd
import os
import random
from fastapi.middleware.cors import CORSMiddleware
import openai
import logging
from langchain.agents import tool
from dotenv import find_dotenv, load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
# from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain_core.messages import AIMessage, HumanMessage
from langchain.prompts.chat import ChatPromptTemplate
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser


load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
CONNECTION_STRING = "postgresql+psycopg2://admin:admin@postgres:5432/vectordb"
COLLECTION_NAME="vectordb"

df = pd.read_csv("Nykaa_Product_Review.csv")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
selected_model = "gpt-3.5-turbo"

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    conversation: List[Message]


embeddings = OpenAIEmbeddings()
model = ChatOpenAI(model =selected_model, temperature=0)

# Agents
pandas_agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0, model=selected_model),
    df,
    verbose=True,
    max_execution_time = 20,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    max_iterations=3
)

@tool
def get_database(query:str):
    '''Useful for when you need to ask anything from Nykaa database containing all products detailed information'''
    ans = pandas_agent.invoke(f'{query}')
    return ans['output']

@tool
def get_orders(query:str):
    '''Useful for when you need to answer regarding orders, returns and complaints'''
    return "I apologize I'm unable to help you regarding orders at the moment. You can visit https://www.nykaafashion.com/sales/order/history for any order related query. Is there anything else I can help you with?"

@tool
def add_cart(query:str):
    '''Useful for when you need to add a product to cart'''
    return "Add to your cart successfully!"

@tool
def shipping_details(product:str):
    '''Useful when you need to answer about shipping details'''
    statements = [
        f"Your product - {product} is arriving today and out for delivery!",
        f"{product} takes 2 business days to ship to Bengaluru city!",
    ]
    return statements[random.randint(0,1)]

tools = [get_database,
        get_orders,
        add_cart,
        shipping_details
        ]

MEMORY_KEY = "chat_history"

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a professional AI Nykaa assistant",
        ),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm_with_tools = model.bind_tools(tools)
chat_history = []

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/service3/{conversation_id}")
async def service3(conversation_id: str, conversation: Conversation):
    inp = conversation.conversation[-1].content
    output = agent_executor.invoke({"input": inp, "chat_history": chat_history})

    # Add to history
    chat_history.extend(
        [
            HumanMessage(content=inp),
            AIMessage(content=output["output"]),
        ]
    )
    return {"id": conversation_id, "reply": output['output']}
