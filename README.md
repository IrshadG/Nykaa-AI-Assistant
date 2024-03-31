# Nykaa-AI-Assistant
A Nykaa chatbot that can suggest products, view order details, add to cart and more.

Please note that this project is still in development.

## About

Numerous RAG based chatbots are now available that can answer queries from a data source like pdf or excel file. These are simple and fall short for an e-commerce AI assistant that can recommend products based on user's preferences, write product reviews and search products using natural language. I created a Nykaa AI assistant that can help you write a review, recommend a product, explain term's and conditions, search a product and more!

## Objective

The AI assistant must follow a flow of control to guide the user and maintain reproducibility.

![Objective](imgs/objective.jpeg?raw=true)

## Process

#### Data

I have used a [Nykaa dataset](https://www.kaggle.com/datasets/susant4learning/nykaacosmeticsproductsreview2021/code) from kaggle as the data source for Nykaa products. It contains most useful data points like product name, rating, description, category and brand, that I required.

![Data](imgs/Data_example.png?raw=true)

#### Frontend

A simple React-JS application that provides the user interface for interacting with the assistant.

![conversation](imgs/conversation-2.png?raw=true)

#### Backend

A Python FastAPI based backend hosting the chatbot algorithm locally. This service communicates with the LLM (OpenAI GPT-3.5-turbo) to process user queries and generate suitable responses. 


The flow of control and AI orchestration is implemented using [Langchain](https://www.langchain.com). For each section of the main functionalities such as product recommendations and product searches, a dedicated tool(tools in langchain are function calls that llms can trigger if they need) is created. These tools may sometimes conatin a chain within the tool.

![conversation](imgs/conversation-1.png?raw=true)

## Usage

To get the project up and running, make sure Docker is installed on your system.

1. Open your .env file and paste your OpenAI_API_Key

2. Run the following command on your terminal in the project directory:

```bash
docker-compose up
```

## Acknowledgement

The architecture of the project is inspired from [this GitHub repo](https://github.com/Coding-Crashkurse/Langchain-Production-Project/tree/main)

