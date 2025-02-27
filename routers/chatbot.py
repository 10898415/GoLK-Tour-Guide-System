import neo4j
from neo4j import GraphDatabase, time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, HTTPException, status, Depends, responses, security, BackgroundTasks, Form
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
from typing import Dict, List
from datetime import datetime
import random
import ast
from fastapi import APIRouter, HTTPException
from pathlib import Path
from openai import OpenAI
from routers import prompts
from routers.prompts import db_structure, settings_prompt
import pandas as pd
from urllib.parse import urlparse
from functools import lru_cache
from typing import Dict, Tuple
import hashlib

chat_histories: Dict[str, Dict[str, List[str]]] = {}

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

load_dotenv()

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
openai_api_key = os.getenv("OPENAI_API_KEY")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-3.5-turbo")
db_structure_prompt = db_structure
settings_prompt = settings_prompt
client = OpenAI(api_key=openai_api_key)

def connect_to_neo4j():
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        driver.verify_connectivity()
        print("Connection to Neo4j established successfully!")
        return driver
    except Exception as e:
        print(f"Failed to connect to Neo4j: {str(e)}")
        return None

driver = connect_to_neo4j()

CURRENT_DIR = Path(__file__).resolve().parent
STATIC_DIR = CURRENT_DIR.parent / "static" / "temp"
os.makedirs(STATIC_DIR, exist_ok=True)

with open('routers/sample.json', 'r') as file:
    data = json.load(file)
    db_questions = [item['question'] for item in data['data']]
    cypher_queries = [item['cypher_query'] for item in data['data']]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(db_questions)

question_cache: Dict[str, dict] = {}

def generate_query(user_question: str, session_id: str, question: Question) -> str:
    recent_history = []
    if session_id in chat_histories:
        questions = chat_histories[session_id]["questions"]
        answers = chat_histories[session_id]["answers"]
        for i in range(max(len(questions) - 4, 0), len(questions) - 1):
            recent_history.append({
                "question": questions[i],
                "answer": answers[i]
            })
    history_text = "No previous conversation." if not recent_history else "\n".join([
        f"Previous Question: {item['question']}\nPrevious Answer: {item['answer']}\n"
        for item in recent_history
    ])
    TEMPLATE_CYPHER = {
        "text_explanation": "",
        "query_generation_status": "Yes/No",
        "query": "OPTIONAL MATCH query here"
    }
    try:
        similar_results = find_similar_questions(user_question)
        similar_text = "\n".join([
            f"Reference Q: {q}\nReference Query: {c}\nSimilarity: {s:.2f}"
            for q, c, s in similar_results
        ])
    except Exception:
        similar_text = "No similar examples found."
    formatted_prompt = QUERY_CHAT_PROMPT.format(
        date=question.date,
        time=question.time,
        history_text=history_text,
        graph_db_structure=db_structure_prompt,
        similar_chunks=similar_text,
        question=user_question,
        template_cypher=TEMPLATE_CYPHER,
        settings_prompt=settings_prompt
    )
    retry_count = 0
    max_retries = 3
    while retry_count < max_retries:
        try:
            chat_messages = [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": formatted_prompt
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_question
                        }
                    ]
                }
            ]
            completion = client.chat.completions.create(
                model=deployment,
                messages=chat_messages,
                max_tokens=4096,
                temperature=question.settings.creativity,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
                stream=False
            )
            return completion.choices[0].message.content
        except Exception as e:
            retry_count += 1
            if retry_count >= max_retries:
                return f"Error after {max_retries} retries: {str(e)}"
            continue
    return "Maximum retries exceeded"

@router.post("/start_session")
async def start_session():
    session_id = str(uuid.uuid4())
    chat_histories[session_id] = {
        "questions": [],
        "answers": []
    }
    return JSONResponse(content={"session_id": session_id})

def serialize_neo4j_value(val):
    if isinstance(val, (neo4j.time.DateTime, neo4j.time.Date)):
        return val.iso_format()
    elif isinstance(val, neo4j.time.Time):
        return str(val)
    elif isinstance(val, (int, float, str, bool)):
        return val
    elif val is None:
        return None
    return str(val)

def serialize_value(val):
    if pd.isna(val):
        return None
    elif isinstance(val, pd.Period):
        return val.asfreq('D').strftime('%Y-%m-%d')
    elif isinstance(val, (pd.Timestamp, datetime)):
        iso_date = val.isoformat()
        if '.' in iso_date:
            iso_date = iso_date.split('.')[0] + 'Z'
        return iso_date
    elif isinstance(val, str):
        try:
            if 'T' in val or '-' in val:
                parsed_date = pd.to_datetime(val)
                return parsed_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        except:
            return val
        return val
    elif isinstance(val, np.integer):
        return int(val)
    elif isinstance(val, np.floating):
        return float(val)
    elif isinstance(val, np.bool_):
        return bool(val)
    elif isinstance(val, (np.ndarray, list)):
        return [serialize_value(v) for v in val]
    elif isinstance(val, dict):
        return {k: serialize_value(v) for k, v in val.items()}
    elif isinstance(val, pd.Index):
        return serialize_value(val.tolist())
    elif isinstance(val, pd.Series):
        return serialize_value(val.tolist())
    elif isinstance(val, pd.DataFrame):
        return serialize_value(val.to_dict('records'))
    elif isinstance(val, pd.DateOffset):
        return str(val)
    elif isinstance(val, pd.Interval):
        return str(val)
    return serialize_neo4j_value(val)

def execute_cypher_query(driver, query):
    try:
        with driver.session() as session:
            result = session.run(query)
            records = []
            for record in result:
                record_dict = {}
                for key, value in dict(record).items():
                    record_dict[key] = serialize_value(value)
                records.append(record_dict)
            return records
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        return None

def generate_table_analysis(data: str):
    try:
        analysis_prompt = f"""
                You are a tourism analytics expert specializing in Sri Lankan travel. 
                If this data contains not only None values return 'yes'.
                If the data only contains null values say you cannot generate an answer with data table at the moment in a creative way with emojis bit longer explanation.
                Don't ever say, since data contains mostly null values or zeros you can't provide an answer.

                example data: 
                    [{{'a1.Areas': None, 'a2.Areas': None, 'a1.Distance_in_km': None}}]

                data : {data}
                """
        completion = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": analysis_prompt},
                {"role": "user", "content": "Please return 'yes' or explanation based on data."}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Unable to provide table insights at this moment. Error: {str(e)}"

def generate_answer_rejection(user_question, question):
    try:
        settings = f"""
                {settings_prompt}
                Response Settings:
               - Language: {question.settings.language}
               - Politeness Level: {question.settings.politeness_level}
               - Formality: {question.settings.formality}
               - Response Length: {question.settings.response_length}
               - Current time: {question.time}
               - Current date: {question.date}

               Please adjust your response according to these settings:
               1. Use the specified {question.settings.language} language
               2. Maintain {question.settings.politeness_level} politeness level
               3. Keep {question.settings.formality} tone
               5. Provide {question.settings.response_length} response length
               6. Use emojis based on above selected settings
               """
        analysis_prompt = f"""You are a tourism analytics expert specializing in Sri Lankan travel. 
                        Say that you cannot generate an answer right now.

                        Original Question: {user_question}

                        Please strictly follow this settings:

                            {settings}
                        """
        completion = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": analysis_prompt},
                {"role": "user", "content": "Please provide the analysis."}
            ],
            max_tokens=1000,
            temperature=question.settings.creativity
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Unable to provide analytical insights at the moment. Error: {str(e)}"

@router.post("/start_session")
async def start_session():
    session_id = str(uuid.uuid4())
    chat_histories[session_id] = {
        "questions": [],
        "answers": []
    }
    return JSONResponse(content={"session_id": session_id})

def cleanup_old_cache(max_age: int = 3600):
    current_time = time.time()
    for key in list(question_cache.keys()):
        if current_time - question_cache[key].get('timestamp', 0) > max_age:
            del question_cache[key]

@router.get("/check_session/{session_id}")
async def check_session(session_id: str):
    if session_id in chat_histories:
        return JSONResponse(
            content={
                "valid": True,
                "session_id": session_id
            }
        )
    return JSONResponse(
        content={"valid": False},
        status_code=404
    )

@router.get("/chat_history/{session_id}")
async def get_chat_history(session_id: str):
    if session_id not in chat_histories:
        return JSONResponse(
            content={"error": "Session not found"},
            status_code=404
        )
    history = []
    questions = chat_histories[session_id]["questions"]
    answers = chat_histories[session_id]["answers"]
    for i in range(len(questions)):
        history.append({
            "sender": "user",
            "text": questions[i],
            "time": datetime.now().strftime("%I:%M %p")
        })
        if i < len(answers):
            try:
                answer_data = answers[i]
                if isinstance(answer_data, str):
                    answer_data = json.loads(answer_data)
                history.append({
                    "sender": "bot",
                    "text": answer_data.get("text_explanation", "No response"),
                    "time": datetime.now().strftime("%I:%M %p"),
                    "tableData": answer_data.get("data"),
                    "tableInsights": answer_data.get("table_insights")
                })
            except Exception as e:
                print(f"Error parsing answer: {str(e)}")
                history.append({
                    "sender": "bot",
                    "text": "Error retrieving response",
                    "time": datetime.now().strftime("%I:%M %p")
                })
    return JSONResponse(content={"history": history})

@router.delete("/end_session/{session_id}")
async def end_session(session_id: str):
    if session_id in chat_histories:
        del chat_histories[session_id]
        return JSONResponse(content={"message": "Session terminated successfully"})
    return JSONResponse(
        content={"error": "Session not found"},
        status_code=404
    )
