from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid
from typing import Dict, List

# In-memory storage for chat histories
chat_histories: Dict[str, Dict[str, List[str]]] = {}

# Create FastAPI router
router = APIRouter()

class Settings(BaseModel):
    language: str
    politeness_level: str
    formality: str
    creativity: float
    response_length: str

class Question(BaseModel):
    question: str
    session_id: str
    settings: Settings
    time: str = None
    date: str = None
    question_history: List[str] = []
    answer_history: List[str] = []

# Load environment variables
load_dotenv()

# Get environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-3.5-turbo")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

@router.post("/start_session")
async def start_session():
    """Initialize a new chat session"""
    session_id = str(uuid.uuid4())
    chat_histories[session_id] = {
        "questions": [],
        "answers": []
    }
    return {"session_id": session_id}

@router.post("/chat")
async def chat(question: Question):
    """Handle chat interactions"""
    try:
        session_id = question.session_id
        user_question = question.question

        # Validate session
        if session_id not in chat_histories:
            raise HTTPException(status_code=400, detail="Invalid session ID")

        # Add question to history
        chat_histories[session_id]["questions"].append(user_question)

        # Create system prompt based on settings
        system_prompt = f"""You are a helpful AI tour guide for Sri Lanka.
        Language: {question.settings.language}
        Politeness: {question.settings.politeness_level}
        Formality: {question.settings.formality}
        Response Length: {question.settings.response_length}
        
        Provide information about Sri Lankan tourism, culture, history, and attractions.
        Be accurate, engaging, and respectful of local customs."""

        # Generate response using OpenAI
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            temperature=question.settings.creativity
        )

        answer = response.choices[0].message.content
        chat_histories[session_id]["answers"].append(answer)

        # Return response with metadata
        return {
            "session_id": session_id,
            "response": answer,
            "timestamp": datetime.now().isoformat(),
            "question_count": len(chat_histories[session_id]["questions"])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    """Retrieve chat history for a session"""
    if session_id not in chat_histories:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return chat_histories[session_id]

@router.delete("/session/{session_id}")
async def end_session(session_id: str):
    """End a chat session and clear its history"""
    if session_id not in chat_histories:
        raise HTTPException(status_code=404, detail="Session not found")
    
    del chat_histories[session_id]
    return {"message": "Session ended successfully"}