"use client";
import { useState, useEffect } from 'react';

const SESSION_KEY = 'chatbot_session_id';

export function useSession() {
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [chatHistory, setChatHistory] = useState([]);

  const loadChatHistory = async (sid) => {
    try {
      const response = await fetch(`/api/session/history?id=${sid}`);
      const data = await response.json();
      if (data.history) {
        setChatHistory(data.history);
      }
    } catch (error) {
      console.error('Failed to load chat history:', error);
    }
  };

  const checkSession = async (sid) => {
    try {
      const response = await fetch(`/api/session/check?id=${sid}`);
      const data = await response.json();
      return data.valid;
    } catch (error) {
      console.error('Failed to check session:', error);
      return false;
    }
  };

  const initSession = async () => {
    try {
      const storedSession = localStorage.getItem(SESSION_KEY);
      
      if (storedSession) {
        // Verify if stored session is still valid
        const isValid = await checkSession(storedSession);
        if (isValid) {
          setSessionId(storedSession);
          await loadChatHistory(storedSession);
          return;
        }
        // If not valid, remove it
        localStorage.removeItem(SESSION_KEY);
      }
      
      // Create new session
      const response = await fetch('/api/session', {
        method: 'GET',
      });
      const data = await response.json();
      
      if (data.session_id) {
        localStorage.setItem(SESSION_KEY, data.session_id);
        setSessionId(data.session_id);
      }
    } catch (error) {
      console.error('Failed to initialize session:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    initSession();
  }, []);

  return { sessionId, loading, chatHistory };
}
