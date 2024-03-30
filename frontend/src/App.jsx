import React, { useState, useEffect } from "react";
import { FaSpinner } from "react-icons/fa";

const App = () => {
  const [conversation, setConversation] = useState({ conversation: [] });
  const [userMessage, setUserMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchConversation = async () => {
      const conversationId = localStorage.getItem("conversationId");
      if (conversationId) {
        const response = await fetch(
          `http://localhost:5000/service2/${conversationId}`
        );
        const data = await response.json();
        if (!data.error) {
          setConversation(data);
        }
      }
    };

    fetchConversation();
  }, []);

  const generateConversationId = () =>
    "_" + Math.random().toString(36).slice(2, 11);

  const handleInputChange = (event) => {
    setUserMessage(event.target.value);
  };

  const handleNewSession = () => {
    localStorage.removeItem("conversationId");
    setConversation({ conversation: [] });
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    let conversationId = localStorage.getItem("conversationId");
    if (!conversationId) {
      conversationId = generateConversationId();
      localStorage.setItem("conversationId", conversationId);
    }

    const newConversation = [
      ...conversation.conversation,
      { role: "user", content: userMessage },
    ];

    const response = await fetch(
      `http://localhost:5000/service2/${conversationId}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ conversation: newConversation }),
      }
    );

    const data = await response.json();
    setConversation(data);
    setUserMessage("");
    setIsLoading(false);
  };

  return (
    <div
      className="App flex flex-col items-center pt-6 min-h-screen bg-gray-900 text-sm"
      style={{
        backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('/images/bg.jpg')`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
    >
      <h1 className="text-3xl font-bold mb-4 text-white"><b>Nykaa AI Assistant</b></h1>
      {conversation.conversation.length > 0 && (
        <div className="flex flex-col p-4 bg-white shadow w-full max-w-md space-y-4 rounded-xl"
        style={
          {backgroundColor: 'rgba(255, 255, 255, 0.7)'}
        }>
          {conversation.conversation
            .filter((message) => message.role !== "system")
            .map((message, index) => (
              <div
                key={index}
                className={`${
                  message.role === "user" ? "text-right rounded-xl p-4" : "text-left rounded-xl p-4"
                }`}
                style={message.role === "user" ? {backgroundColor: "#A04B79"} : {backgroundColor: "#DA68A6"}}
              >
                <strong className="font-bold text-white px-2">
                  {message.role}:
                </strong>
                <span className="text-white">{message.content}</span>
              </div>
            ))}
        </div>
      )}
      <div className="flex flex-row w-full max-w-md mt-4">
        <input
          type="text"
          value={userMessage}
          onChange={handleInputChange}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              event.preventDefault();
              handleSubmit();
            }
          }}
          className="flex-grow mr-4 p-4 rounded-xl h-12 border-gray-300"
          placeholder={isLoading ? "Processing..." : "Type your message here"}
        />
        <button
          onClick={handleSubmit}
          disabled={isLoading}
          className="p-2 w-24 h-12 rounded-xl text-white"
          style={ 
            { backgroundColor: "#D666A9" }}
        >
        Send
        </button>
      </div>
      {isLoading && (
        <div className="flex items-center space-x-4 text-l text-white">
          <FaSpinner className="animate-spin" />
          <span>Loading...</span>
        </div>
      )}
      <button
        onClick={handleNewSession}
        className="mt-4 py-2 h-12 px-6 rounded-xl text-white absolute top-0 left-4"
        style={ 
          { backgroundColor: "#D59465" }}
      >
        New Session
      </button>
    </div>
  );
};

export default App;
