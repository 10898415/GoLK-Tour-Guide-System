"use client";
import { useState, useEffect } from "react";
import { useSession } from "../hooks/useSession";
import TableView from "./TableView";
import ReactMarkdown from 'react-markdown';

export default function ChatArea() {
  const { sessionId, loading, chatHistory } = useSession();
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hi, I'm TourMate. How can I help you today?",
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      avatar: "/botAvatar.png",
    },
  ]);

  // Initialize messages with chat history when it's loaded
  useEffect(() => {
    if (chatHistory.length > 0) {
      const formattedHistory = chatHistory.map(msg => ({
        ...msg,
        avatar: msg.sender === "bot" ? "/botAvatar.png" : "/userAvatar.png"
      }));
      setMessages([messages[0], ...formattedHistory]); // Keep welcome message
    }
  }, [chatHistory]);

  const [input, setInput] = useState("");

  const renderMessage = (msg, index) => {
    return (
      <div key={index} className={`flex mb-3 ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
        {msg.sender !== "user" && (
          <img src={msg.avatar} alt="avatar" className="h-8 w-8 rounded-full mr-2 object-cover" />
        )}
        <div className="flex flex-col max-w-3xl">
          <div className={`rounded-md p-3 ${msg.sender === "user" ? "bg-blue-100" : "bg-gray-100"}`}>
            <div className="mb-1 text-sm prose prose-sm max-w-none prose-strong:text-inherit prose-em:text-inherit prose-headings:text-inherit">
              <ReactMarkdown>{msg.text}</ReactMarkdown>
            </div>
            <p className="text-xs text-gray-500">{msg.time}</p>
          </div>
          {msg.tableData && (
            <TableView 
              data={msg.tableData} 
              insights={msg.tableInsights}
            />
          )}
        </div>
        {msg.sender === "user" && (
          <img src={msg.avatar} alt="avatar" className="h-8 w-8 rounded-full ml-2 object-cover" />
        )}
      </div>
    );
  };

  const handleSend = async () => {
    if (!input.trim() || !sessionId) return;

    const userMessage = {
      sender: "user",
      text: input,
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      avatar: "/userAvatar.png",
    };
    setMessages(prev => [...prev, userMessage]);
    setInput("");

    try {
      const res = await fetch("/api/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: input,
          session_id: sessionId
        }),
      });
      const data = await res.json();

      const botMessage = {
        sender: "bot",
        text: data.reply,
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        avatar: "/botAvatar.png",
        tableData: data.tableData,
        tableInsights: data.tableInsights
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Sorry, I couldn't process your request.",
          time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
          avatar: "/botAvatar.png",
        },
      ]);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-[60vh]">
      <p>Loading chat...</p>
    </div>;
  }

  return (
    <div className="bg-white rounded-md shadow p-4">
      <div className="max-h-[60vh] overflow-y-auto mb-4">
        {messages.map((msg, index) => renderMessage(msg, index))}
      </div>
      
      <div className="flex items-center space-x-2">
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          className="flex-1 border border-gray-300 p-2 rounded focus:outline-none"
        />
        <button 
          onClick={handleSend} 
          className="bg-black text-white px-4 py-2 rounded hover:bg-gray-800"
        >
          Send
        </button>
      </div>
    </div>
  );
}
