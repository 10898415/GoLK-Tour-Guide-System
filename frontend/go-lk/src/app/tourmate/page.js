"use client";
import { useState, useEffect, useRef } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation'
import { useSession } from "../hooks/useSession";
import TableView from "../components/TableView";

export default function TourMatePage() {
  const { sessionId, loading } = useSession();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [language, setLanguage] = useState("English"); // Default language
  const [suggestedQuestions, setSuggestedQuestions] = useState([
    "What are the top attractions in Kandy?",
    "Find hotels near Sigiriya",
    "What's the weather like in Galle in December?",
    "Emergency contacts in Colombo"
  ]);
  const [hasAutoSent, setHasAutoSent] = useState(false);
  const [queuedMessage, setQueuedMessage] = useState(null);
  const messagesEndRef = useRef(null);
  const searchParams = useSearchParams()
  
  // Available languages
  const languages = [
    "English",
    "සිංහල", // Sinhala
    "Français (French)", // French
    "Русский (Russian)" , // Russian
    "日本語 (Japanese)", // Japanese
    "한국어 (Korean)", // Korean
    "中文 (Chinese)", // Chinese
    "Українська (Ukrainian)", // Ukrainian
    "हिन्दी (Hindi)", // Hindi
    "தமிழ் (Tamil)", // Tamil
    "Nederlands (Dutch)" // Dutch
  ];
  
  // Function to map display language to backend language
  const getBackendLanguage = (displayLanguage) => {
    const languageMap = {
      "English": "English",
      "සිංහල": "Sinhala",
      "Français (French)": "French",
      "Русский (Russian)": "Russian",
      "日本語 (Japanese)": "Japanese",
      "한국어 (Korean)": "Korean",
      "中文 (Chinese)": "Chinese",
      "Українська (Ukrainian)": "Ukrainian",
      "हिन्दी (Hindi)": "Hindi",
      "தமிழ் (Tamil)": "Tamil",
      "Nederlands (Dutch)": "Dutch"
    };
    return languageMap[displayLanguage] || "English";
  };
  
  useEffect(() => {
    if (!loading && sessionId) {
      // Initialize with welcome message if no messages exist
      if (messages.length === 0) {
        setMessages([{
          id: "welcome",
          sender: "bot",
          text: "Hi, I'm TourMate! I can help you discover Sri Lanka - from finding hotels and attractions to locating emergency services. How can I assist with your travel plans today?",
          time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        }]);
      }
    }
  }, [loading, sessionId, messages.length]);

  // Only scroll if messages have been added (not on initial load)
  useEffect(() => {
    if (messages.length > 0) {
      // Use a small timeout to ensure DOM has updated
      const timer = setTimeout(() => {
        messagesEndRef.current?.scrollIntoView({ 
          behavior: "smooth",
          block: "end"  // Ensures it aligns to the end of the container
        });
      }, 100);
      
      return () => clearTimeout(timer);
    }
  }, [messages]);

  const handleSendMessage = async () => {
    console.log("Sending message:", input);
    if (!input.trim() || !sessionId) return;

    const userMessage = {
      id: `user-${Date.now()}`,
      sender: "user",
      text: input,
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    // Add user message to chat immediately
    setMessages(prev => [...prev, userMessage]);
    
    // Save current input and clear the input field
    const currentInput = input;
    setInput("");
    setIsTyping(true);

    try {
      // Map the display language to backend language
      const backendLanguage = getBackendLanguage(language);
      
      // Log the request for debugging
      console.log("Sending chat request:", {
        message: currentInput,
        session_id: sessionId,
        language: language,
        backendLanguage: backendLanguage
      });

      const response = await fetch("/api/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: currentInput,
          session_id: sessionId,
          language: backendLanguage  // Send the mapped language to the backend
        }),
      });

      // Check if the response is ok
      if (!response.ok) {
        const errorText = await response.text();
        console.error("Error response:", response.status, errorText);
        throw new Error(`Request failed with status ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      console.log("Received response:", data);

      // Simulate typing delay for more natural interaction
      setTimeout(() => {
        setIsTyping(false);
        
        const botMessage = {
          id: `bot-${Date.now()}`,
          sender: "bot",
          text: data.reply || "I'm sorry, I don't have a response for that.",
          time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
          tableData: data.tableData,
          tableInsights: data.tableInsights
        };
        
        setMessages(prev => [...prev, botMessage]);
        
        // Update suggested questions based on context
        if (currentInput.toLowerCase().includes("hotel") || currentInput.toLowerCase().includes("stay")) {
          setSuggestedQuestions([
            "What amenities are included?",
            "Is breakfast included?",
            "How far is it from attractions?",
            "What's the cancellation policy?"
          ]);
        } else if (currentInput.toLowerCase().includes("beach") || currentInput.toLowerCase().includes("swimming")) {
          setSuggestedQuestions([
            "Are there lifeguards?",
            "Best beaches for surfing?",
            "Beach restaurants nearby?",
            "Which beaches are less crowded?"
          ]);
        }
      }, 1500);
    } catch (error) {
      console.error("Error sending message:", error);
      setIsTyping(false);
      
      setMessages(prev => [...prev, {
        id: `error-${Date.now()}`,
        sender: "bot",
        text: "I'm sorry, I couldn't process your request. Please try again later.",
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      }]);
    }
  };

  // Auto enter first chat if the message search parameter exists
  useEffect(() => {
    const askMessage = searchParams.get('message');
    if (askMessage && !hasAutoSent && !loading) {
      setQueuedMessage(askMessage);
      setInput(askMessage);
      setHasAutoSent(true); // prevent re-running
    }
  }, [searchParams, hasAutoSent, loading]);

  useEffect(() => {
    if (queuedMessage && input === queuedMessage) {
      handleSendMessage();
      setQueuedMessage(null); // clear queued message
    }
  }, [input, queuedMessage]);

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };
  
  const handleSuggestedQuestion = (question) => {
    setInput(question);
    // Automatically send the suggested question
    setTimeout(() => {
      handleSendMessage();
    }, 100);
  };

  if (loading) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="mt-4 text-gray-600">Connecting to TourMate...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-[80vh] bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          {/* Chat Header */}
          <div className="bg-emerald-700 p-4 flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-10 h-10 relative">
                <Image 
                  src="/images/botAvatar.png" 
                  alt="TourMate Avatar" 
                  fill
                  className="object-cover rounded-full"
                />
              </div>
              <div className="ml-3">
                <div className="flex items-center">
                  <h2 className="text-white font-bold">TourMate</h2>
                  <div className="flex items-center ml-2">
                    <div className="h-2 w-2 rounded-full bg-green-400 mr-1"></div>
                    <span className="text-emerald-100 text-sm">Online</span>
                  </div>
                </div>
                <p className="text-emerald-100 text-sm">Your Sri Lankan Travel Assistant</p>
              </div>
            </div>
            
            {/* Language Selector - Positioned on the right */}
            <div className="flex items-center">
              <span className="text-white text-sm mr-2">Language:</span>
              <select
                value={language}
                onChange={handleLanguageChange}
                className="bg-emerald-600 text-white border border-emerald-500 rounded-md py-1 px-2 text-sm focus:outline-none focus:ring-1 focus:ring-white"
              >
                {languages.map((lang) => (
                  <option key={lang} value={lang}>
                    {lang}
                  </option>
                ))}
              </select>
            </div>
          </div>
          
          {/* Chat Messages */}
          <div className="h-[calc(70vh-120px)] overflow-y-auto p-4 bg-gray-50" style={{ scrollBehavior: 'smooth' }}>
            {messages.map((message) => (
              <div key={message.id} className={`mb-4 flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                {message.sender === 'bot' && (
                  <div className="w-8 h-8 relative rounded-full overflow-hidden flex-shrink-0 mr-2">
                    <Image 
                      src="/images/botAvatar.png" 
                      alt="TourMate Avatar" 
                      fill
                      className="object-cover"
                    />
                  </div>
                )}
                
                <div className={`max-w-[80%] ${message.sender === 'user' ? 'order-1' : 'order-2'}`}>
                  <div className={`p-4 rounded-lg ${
                    message.sender === 'user' 
                      ? 'bg-emerald-600 text-white rounded-tr-none' 
                      : 'bg-white shadow rounded-tl-none'
                  }`}>
                    <div className="whitespace-pre-wrap text-sm mb-2">{message.text}</div>
                    <div className={`text-xs ${message.sender === 'user' ? 'text-emerald-100' : 'text-gray-500'}`}>
                      {message.time}
                    </div>
                  </div>
                  
                  {/* Display table data if available */}
                  {message.tableData && (
                    <div className="mt-2">
                      <TableView
                        data={message.tableData}
                        insights={message.tableInsights}
                      />
                    </div>
                  )}
                </div>
                
                {message.sender === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-gray-300 overflow-hidden flex-shrink-0 ml-2 relative">
                    <Image 
                      src="/images/userAvatar.png" 
                      alt="User" 
                      fill
                      className="object-cover"
                    />
                  </div>
                )}
              </div>
            ))}
            
            {/* Typing indicator */}
            {isTyping && (
              <div className="flex items-center mb-4">
                <div className="w-8 h-8 relative rounded-full overflow-hidden flex-shrink-0 mr-2">
                  <Image 
                    src="/images/tourmate-avatar.png" 
                    alt="TourMate Avatar" 
                    fill
                    className="object-cover"
                  />
                </div>
                <div className="bg-white p-3 rounded-lg shadow inline-flex">
                  <div className="typing">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
          
          {/* Suggested Questions */}
          <div className="px-4 py-2 border-t border-gray-200">
            <div className="flex flex-wrap gap-2">
              {suggestedQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestedQuestion(question)}
                  className="bg-gray-100 hover:bg-gray-200 text-gray-800 text-sm px-3 py-1 rounded-full transition-colors"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
          
          {/* Input Area */}
          <div className="p-4 border-t border-gray-200 flex">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Type your message here..."
              className="flex-1 border border-gray-300 rounded-lg resize-none px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              rows="2"
            />
            <button
              onClick={handleSendMessage}
              disabled={!input.trim()}
              className={`ml-3 px-4 rounded-lg flex items-center justify-center ${
                input.trim() 
                  ? 'bg-emerald-600 hover:bg-emerald-700 text-white' 
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
              </svg>
            </button>
          </div>
        </div>
        
        {/* Information Panel */}
        <div className="mt-8 bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Getting the Most from TourMate</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex">
              <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div className="ml-4">
                <h4 className="font-bold text-gray-800">Be Specific</h4>
                <p className="text-gray-600 text-sm">Ask specific questions about locations, activities, or services you're interested in.</p>
              </div>
            </div>
            
            <div className="flex">
              <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                </svg>
              </div>
              <div className="ml-4">
                <h4 className="font-bold text-gray-800">Follow-up Questions</h4>
                <p className="text-gray-600 text-sm">Continue the conversation by asking more details about TourMate's responses.</p>
              </div>
            </div>
            
            <div className="flex">
              <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <h4 className="font-bold text-gray-800">Local Insights</h4>
                <p className="text-gray-600 text-sm">Ask about local customs, best times to visit, or hidden gems in Sri Lanka.</p>
              </div>
            </div>
            
            <div className="flex">
              <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              <div className="ml-4">
                <h4 className="font-bold text-gray-800">Emergency Help</h4>
                <p className="text-gray-600 text-sm">In case of emergency, ask TourMate for nearby hospitals, police stations, or embassy contacts.</p>
              </div>
            </div>
          </div>
          
          <div className="mt-6 pt-6 border-t border-gray-200">
            <p className="text-gray-600 text-sm">
              TourMate uses real-time data from our Neo4j graph database to provide you with the most accurate and up-to-date information about Sri Lanka. If you have any feedback or suggestions, please let us know!
            </p>
          </div>
        </div>
      </div>
      
      {/* Add custom styles for the typing animation */}
      <style jsx>{`
        .typing {
          display: flex;
          align-items: center;
        }
        .typing span {
          height: 8px;
          width: 8px;
          background: #3f6212;
          border-radius: 50%;
          display: inline-block;
          margin-right: 3px;
          animation: pulse 1.5s infinite ease-in-out;
        }
        .typing span:nth-child(2) {
          animation-delay: 0.2s;
        }
        .typing span:nth-child(3) {
          animation-delay: 0.4s;
          margin-right: 0;
        }
        @keyframes pulse {
          0%, 100% {
            transform: scale(0.8);
            opacity: 0.5;
          }
          50% {
            transform: scale(1.2);
            opacity: 1;
          }
        }
      `}</style>
    </div>
  );
}