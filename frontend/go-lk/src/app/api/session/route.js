import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://127.0.0.1:8000';

export async function GET() {
  try {
    const response = await fetch(`${BACKEND_URL}/api/start_session`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      }
    });

    if (!response.ok) {
      throw new Error(`Backend responded with status: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
    
  } catch (error) {
    console.error("Error in session API route:", error);
    
    const errorMessage = error.cause?.code === 'ECONNREFUSED' 
      ? "Cannot connect to backend server. Please ensure it's running."
      : "Internal server error";
      
    return NextResponse.json(
      { error: errorMessage }, 
      { status: 500 }
    );
  }
}
