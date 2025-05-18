import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://127.0.0.1:8000';

export async function GET(request) {
  try {
    // Extract session ID from URL
    const sessionId = request.nextUrl.searchParams.get('id');
    if (!sessionId) {
      return NextResponse.json({ valid: false }, { status: 400 });
    }

    const response = await fetch(`${BACKEND_URL}/chatbot/check_session/${sessionId}`, {
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      }
    });

    const data = await response.json();
    return NextResponse.json(data);
    
  } catch (error) {
    console.error("Error checking session:", error);
    return NextResponse.json({ valid: false }, { status: 500 });
  }
}
