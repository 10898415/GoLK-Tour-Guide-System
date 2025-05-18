import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://127.0.0.1:8000';

export async function POST(req) {
  try {
    const body = await req.json();
    const { message, session_id, language } = body;

    if (!message) {
      return NextResponse.json(
        { error: "Message is required!" },
        { status: 400 }
      );
    }

    if (!session_id) {
      return NextResponse.json(
        { error: "Session ID is required!" },
        { status: 400 }
      );
    }

    const currentDate = new Date();
    
    // Forward request to your backend
    const backendResponse = await fetch(`${BACKEND_URL}/api/chat`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({
        question: message,
        session_id: session_id,
        settings: {
          language: language || "English",  // Use the mapped language parameter
          politeness_level: "Friendly",
          formality: "Casual",
          creativity: 0.7,
          response_length: "Medium"
        },
        date: currentDate.toISOString().split('T')[0],
        time: currentDate.toLocaleTimeString()
      })
    });

    if (!backendResponse.ok) {
      console.error("Error in chatbot API route:", await backendResponse.text());
      throw new Error(`Backend responded with status: ${backendResponse.status}`);
    }

    const data = await backendResponse.json();
    return NextResponse.json({
      reply: data.result?.text_explanation || "No response",
      tableData: data.result?.data || null,
      tableInsights: data.result?.table_insights || null
    });
    
  } catch (error) {
    console.error("Error in chatbot API route:", error);
    
    // More descriptive error for debugging
    const errorMessage = error.cause?.code === 'ECONNREFUSED' 
      ? "Cannot connect to backend server. Please ensure it's running."
      : "Internal server error";
      
    return NextResponse.json(
      { reply: errorMessage }, 
      { status: 500 }
    );
  }
}