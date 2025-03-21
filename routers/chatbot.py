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

# In-memory storage for chat histories
chat_histories: Dict[str, Dict[str, List[str]]] = {}

# Create FastAPI instance
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
uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
openai_api_key = os.getenv("OPENAI_API_KEY")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-3.5-turbo")
db_structure_prompt = db_structure
settings_prompt = settings_prompt
client = OpenAI(api_key=openai_api_key)

# Function to connect to Neo4j
def connect_to_neo4j():
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password)) # Connect to the Neo4j database
        driver.verify_connectivity() # Verify the connection
        print("Connection to Neo4j established successfully!")
        return driver
    except Exception as e:
        print(f"Failed to connect to Neo4j: {str(e)}") # Print the error message
        return None

# Connect to Neo4j
driver = connect_to_neo4j()

# Get the current file's directory and set up static path
CURRENT_DIR = Path(__file__).resolve().parent
STATIC_DIR = CURRENT_DIR.parent / "static" / "temp"
os.makedirs(STATIC_DIR, exist_ok=True)




vectorizer = TfidfVectorizer()
# Pre-compute TF-IDF matrix for existing questions
tfidf_matrix = vectorizer.fit_transform(db_questions)

# Cache for storing previously generated responses
question_cache: Dict[str, dict] = {}


@lru_cache(maxsize=1000)
def find_similar_questions_cached(user_query: str, top_n: int = 5) -> Tuple[tuple]:
    """Cached version of find_similar_questions"""
    results = find_similar_questions(user_query, top_n)
    return tuple(results)


def generate_query_optimized(user_question: str, session_id: str, question: Question) -> str:
    # Create a cache key based on the question and settings
    cache_key = hashlib.md5(
        f"{user_question}_{question.settings.json()}".encode()
    ).hexdigest()

    # Check cache first
    if cache_key in question_cache:
        return question_cache[cache_key]

    # If not in cache, generate response
    response = generate_query(user_question, session_id, question)

    # Store in cache
    question_cache[cache_key] = response

    return response


def find_similar_questions(user_query, top_n=5):
    """Find similar questions using pre-computed TF-IDF matrix"""
    global tfidf_matrix, vectorizer, db_questions, cypher_queries

    try:
        # Transform only the user query using the pre-computed vectorizer
        query_vector = vectorizer.transform([user_query])

        # Compute similarity with pre-computed matrix
        similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

        # Get top N similar indices
        similar_indices = similarities.argsort()[-top_n:][::-1]

        # Return results
        similar_questions = [
            (db_questions[i], cypher_queries[i], similarities[i])
            for i in similar_indices
        ]

        print(similar_questions)

        return similar_questions

    except Exception as e:
        print(f"Error in finding similar questions: {str(e)}")
        return []


def generate_query(user_question: str, session_id: str, question: Question) -> str:
    recent_history = []  # Initialize an empty list to store recent conversation history
    if session_id in chat_histories:  # Check if the session ID exists in the chat histories
        questions = chat_histories[session_id]["questions"]  # Get the questions from the chat histories
        answers = chat_histories[session_id]["answers"]  # Get the answers from the chat histories
        # Get the last 3 items, excluding the current question
        for i in range(max(len(questions) - 4, 0), len(questions) - 1):
            recent_history.append({
                "question": questions[i],
                "answer": answers[i]
            })

    # Format the conversation history
    history_text = "No previous conversation." if not recent_history else "\n".join([
        f"Previous Question: {item['question']}\n"
        f"Previous Answer: {item['answer']}\n"
        for item in recent_history
    ])

    # Define template as a constant
    TEMPLATE_CYPHER = {
        "text_explanation": "",
        "query_generation_status": "Yes/No",
        "query": "OPTIONAL MATCH query here"
    }



    # Move the prompt template outside the function
    QUERY_CHAT_PROMPT = """Role and Context:
                        You are TourMate, an AI assistant that helps users with travel-related queries about Sri Lanka.
                        
                        Recent Conversation History: (This contains the recent questions user asked)
                        -------------------------
                        {history_text}
                        
                         Database Context:
                        ---------------
                        Current Graph Database Structure: {graph_db_structure}
                        
                        Reference Examples (Not Part of Current Conversation or history):
                        -------------------------
                        Reference Examples : {similar_chunks}
                        
                          
                       ⚠️ Note: These examples are ONLY for cypher query generation reference. Do not use Reference Examples as conversation history or general content.
                       Very Very Important: ⚠️⚠️ Do Not ever use the same reference examples to generate your answer, because it is not the answer user is expecting. 
                       it is given to get an idea of the cypher query structure.
                        Query Requirements:
                        -----------------
                        1. All queries must start with OPTIONAL MATCH
                        2. Only use nodes, elements, and relationships defined in the provided graph structure
                        3. Support cross-table filtering when necessary
                        
                        Today Date:
                        ---------------
                        {date}
                        
                        Today Time:
                        ______________
                        {time}
                        
                        Input Question:
                        --------------
                        {question}
                        
                        Response Format:
                        --------------
                        IMPORTANT: Return ONLY the following structure in valid JSON format:
                        - Use double quotes (") instead of single quotes (')
                        - No newlines within values
                        - No trailing commas
                        - Exactly match this structure:
                        
                        {template_cypher}
                        
                        ⚠️ DO NOT include any text before or after the JSON structure
                        ⚠️ DO NOT use single quotes in the JSON response
                        ⚠️ DO NOT include newlines within the values
                        ⚠️ Ensure the response is valid JSON format
                        
                        Response Guidelines:
                        ------------------
                        1. text_explanation:
                           - Provide natural language explanations
                           - Can include emojis for better readability
                           - Must NOT contain code or queries
                           - For general questions, provide complete, knowledgeable answers here
                           - For data-related questions, focus on insights and business impact
                           - Never mention querying or accessing a database
                           - Maintain a conversational, helpful tone
                           - Provide natural language explanations ONLY about Sri Lanka
                           - Must be strictly related to Sri Lanka operations and services
                           - Must NOT contain any political, controversial, or Sri Lanka content
                           - For general questions, ONLY provide answers related to Sri Lanka
                           - Maintain a professional, business-focused tone
                           - ** Must contain emojis for better readability
                           - ⚠️⚠️ Do not explain the query that you are generating, explain the answer to the user question.
                        
                        2. query_generation_status:
                           - 'Yes': If a Cypher query can be generated based on the question and graph structure
                           - 'No': If question cannot be answered with a query if keywords are not present in the question
                           - If 'No', query field should be empty
                           
                        3. query structure details:
                           - ⚠️ Do not ever provide multiple relations in one line (Always use multiple OPTIONAL MATCH with WITH clause)
                           - ⚠️⚠️ Do not ever return nodes, always return properties of nodes (This is very important)
                           
                        # Stay Focused and Contextual
                        - Provide responses that are strictly relevant to the questions asked about Sri Lanka
                        - Do not include any information beyond the scope of the specific query or subject matter being discussed
                        - Avoid providing out-of-context or irrelevant information in any responses
                        - Maintain focus on the exact question asked and its direct implications for Sri Lanka
                        - If question is unclear, ask for clarification rather than making assumptions
                        - Never add extraneous information not directly related to the query
                        - Relevant emojis is Must in the text explanation and never mention that you refer to database by querying. 
                        -  Work as TravelGuru when providing responses.
                        
                        # Strictly follow this setting prompts as well
                        {settings_prompt}  
                        """

    retry_count = 0  # Initialize retry count
    max_retries = 2  # Set maximum number of retries

    try:
        similar_results = find_similar_questions(user_question)
        similar_text = "\n".join([
            f"Reference Q: {q}\nReference Query: {c}\nSimilarity: {s:.2f}"
            for q, c, s in similar_results
        ])
    except Exception as e:
        similar_text = "No similar examples found."

        # Format the prompt with all required values
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


    # Retry loop for API call
    while retry_count < max_retries:
        try:
            # Construct chat messages
            chat_messages = [
                {
                    "role": "system",  # System role for the AI assistant
                    "content": [  # Content of the message
                        {
                            "type": "text",
                            "text": formatted_prompt  # Add the formatted prompt to the content
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_question  # Add the user question to the content
                        }
                    ]
                }
            ]

            # Make API call
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

            # Check if the response contains the query generation status
            return completion.choices[0].message.content

        # Retry on API errors
        except Exception as e:
            retry_count += 1
            if retry_count >= max_retries:
                return f"Error after {max_retries} retries: {str(e)}"
            continue
    # Return error message if maximum retries exceeded
    return "Maximum retries exceeded"


# Define the FastAPI router
@router.post("/start_session")
async def start_session():
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    chat_histories[session_id] = {
        "questions": [],
        "answers": []
    }
    return JSONResponse(content={"session_id": session_id})  # Return the session ID as JSON


# Define the FastAPI router
def serialize_neo4j_value(val):
    """Serialize Neo4j specific data types"""
    if isinstance(val, (neo4j.time.DateTime, neo4j.time.Date)): # Check for DateTime or Date objects
        return val.iso_format()
    elif isinstance(val, neo4j.time.Time): # Check for Time objects
        return str(val)
    elif isinstance(val, (int, float, str, bool)): # Check for basic data types
        return val
    elif val is None:
        return None
    return str(val)

# Define the FastAPI router
def serialize_value(val):
    """Main serialization function for all types"""
    if pd.isna(val):
        return None
    # Handle pandas Period objects
    elif isinstance(val, pd.Period):
        return val.asfreq('D').strftime('%Y-%m-%d')
    # Handle both datetime and Timestamp objects
    elif isinstance(val, (pd.Timestamp, datetime)):
        # Convert to ISO format and truncate microseconds if present
        iso_date = val.isoformat()
        if '.' in iso_date:
            iso_date = iso_date.split('.')[0] + 'Z'
        return iso_date
    elif isinstance(val, str):
        # Try to parse string as datetime if it looks like a date
        try:
            if 'T' in val or '-' in val:
                parsed_date = pd.to_datetime(val)
                return parsed_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        except:
            return val
    elif isinstance(val, np.integer): # Handle numpy integer types
        return int(val)
    elif isinstance(val, np.floating): # Handle numpy float types
        return float(val)
    elif isinstance(val, np.bool_): # Handle numpy boolean types
        return bool(val)
    elif isinstance(val, (np.ndarray, list)): # Handle numpy arrays and lists
        return [serialize_value(v) for v in val]
    elif isinstance(val, dict): # Handle dictionaries
        return {k: serialize_value(v) for k, v in val.items()}
    elif isinstance(val, pd.Index): # Handle pandas Index objects
        return serialize_value(val.tolist())
    elif isinstance(val, pd.Series): # Handle pandas Series objects
        return serialize_value(val.tolist())
    elif isinstance(val, pd.DataFrame): # Handle pandas DataFrame objects
        return serialize_value(val.to_dict('records'))
    elif isinstance(val, pd.DateOffset): # Handle pandas DateOffset objects
        return str(val)
    elif isinstance(val, pd.Interval): # Handle pandas Interval objects
        return str(val)
    return serialize_neo4j_value(val) # Fallback to Neo4j serialization


# Define the FastAPI router
def execute_cypher_query(driver, query):
    """Execute a Cypher query and return serialized results"""
    try:
        with driver.session() as session:
            result = session.run(query)
            # Convert Neo4j records to dictionaries and serialize the values
            records = []
            for record in result:
                # Convert each record to a dict and serialize all values
                record_dict = {}
                for key, value in dict(record).items(): # Convert to dict to access items
                    record_dict[key] = serialize_value(value)
                records.append(record_dict) # Append the serialized record to the list
            return records
    except Exception as e: # Handle any exceptions
        print(f"Error executing query: {str(e)}")
        return None

def make_url_link(value):
    """Convert URL to a clickable link."""
    if pd.isna(value):
        return ""

    value_str = str(value).strip()

    # Basic URL validation
    try:
        result = urlparse(value_str)
        is_valid = all([result.scheme, result.netloc])
    except:
        is_valid = False

    if not is_valid:
        return value_str

    return f'<a href="{value_str}" style="color: #0066cc; text-decoration: none;" target="_blank">{value_str}</a>'

def convert_to_html_table(data):
    """Convert data to HTML table with clickable links."""
    if not data:
        return ""

    # Convert data to pandas DataFrame
    df = pd.DataFrame(data)

    # Identify URL columns
    url_columns = [col for col in df.columns if any(term in col.lower()
                                                    for term in ['url', 'link', 'website', 'site'])]

    # Apply URL link conversion
    for col in url_columns:
        df[col] = df[col].apply(make_url_link)

    # Generate HTML table
    html_table = df.to_html(
        classes=['table', 'table-striped', 'table-hover', 'table-bordered'],
        index=False,
        escape=False,
        table_id='result-table'
    )

    # Add CSS styling
    html_table = html_table.replace(
        '<table',
        '<table style="border-collapse: collapse; border: 1px solid black; width: 100%;"'
    )
    html_table = html_table.replace(
        '<th',
        '<th style="border: 1px solid black; text-align: center; padding: 8px; background-color: #f5f5f5;"'
    )
    html_table = html_table.replace(
        '<td',
        '<td style="border: 1px solid black; text-align: left; padding: 8px; vertical-align: top;"'
    )

    return html_table


# Function to generate a Cypher query based on the user question
def generate_table_analysis(data: str):
    try:
        # Prepare prompt for LLM
        analysis_prompt = f"""
                You are a tourism analytics expert specializing in Sri Lankan travel. 
                If this data contains not only None values return 'yes'.
                If the data only contains null values say you cannot generate an answer with data table at the moment in a creative way with emojis bit longer explanation.
                Don't ever say, since data contains mostly null values or zeros you can't provide an answer.

                example data: 
                    [{{'a1.Areas': None, 'a2.Areas': None, 'a1.Distance_in_km': None}}]
                # If it is like this also say you cannot generate an answer at this moment bit longer ways.

                data : {data}
                """

        # Make API call
        completion = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": analysis_prompt},
                {"role": "user", "content": "Please return 'yes' or explanation based on data."}
            ],
            max_tokens=1000,  # Set maximum tokens for response
            temperature=0.7  # Set the creativity level
        )

        return completion.choices[0].message.content  # Return the generated analysis
    except Exception as e:
        return f"Unable to provide table insights at this moment. Error: {str(e)}"


# Function to generate a Cypher query based on the user question
def generate_html_table_analysis(data, user_question, deployment, question):
    try:
        # Prepare settings prompt for the user
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

        # Prepare prompt for LLM
        analysis_prompt = f"""You are a tourism analytics expert specializing in Sri Lankan travel. 
                        Analyze the following data in context of the user's question and provide 3-4 key tourism insights in an interactive way.
                        Do not describe about links provided.
                        Do not provide any welcome statements.

                        Original Question: {user_question}
                        Data: {str(data)}
                        
                        Format your response as a direct list of insights without any preamble or introduction.
                        
                        Please strictly follow this settings:
                           
                            {settings}
                        """

        # Make API call
        completion = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": analysis_prompt},
                {"role": "user", "content": "Please provide the analysis."}
            ],
            max_tokens=1000,  # Set maximum tokens for response
            temperature=question.settings.creativity  # Set the creativity level based on user settings
        )

        return completion.choices[0].message.content  # Return the generated analysis

    except Exception as e:  # Handle any exceptions
        return f"Unable to provide analytical insights at the moment. Error: {str(e)}"


# Function to generate a Cypher query based on the user question
def generate_answer_rejection(user_question, question):
    try:
        # Prepare settings prompt for the user
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

        # Prepare prompt for LLM
        analysis_prompt = f"""You are a tourism analytics expert specializing in Sri Lankan travel. 
                        Say that you cannot generate an answer right now.

                        Original Question: {user_question}

                        Please strictly follow this settings:

                            {settings}
                        """

        # Make API call
        completion = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": analysis_prompt},
                {"role": "user", "content": "Please provide the analysis."}
            ],
            max_tokens=1000,  # Set maximum tokens for response
            temperature=question.settings.creativity  # Set the creativity level based on user settings
        )

        return completion.choices[0].message.content  # Return the generated analysis

    except Exception as e:  # Handle any exceptions
        return f"Unable to provide analytical insights at the moment. Error: {str(e)}"


# Define the FastAPI router
@router.post("/start_session")
async def start_session():
    session_id = str(uuid.uuid4()) # Generate a unique session ID
    chat_histories[session_id] = {
        "questions": [],
        "answers": []
    }
    return JSONResponse(content={"session_id": session_id}) # Return the session ID as JSON


@router.post("/chat")
async def chat(question: Question):
    try:
        # Extract the required information from the question object
        session_id = question.session_id # Extract the session ID
        user_question = question.question # Extract the user question
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") # Extract the current timestamp

        # Check if the session ID is valid
        if session_id not in chat_histories:
            return JSONResponse(
                content={"error": "Invalid session ID"},
                status_code=400
            )

        # Add the user question to the chat history
        chat_histories[session_id]["questions"].append(user_question)
        

        # Get the query generation response
        query_response = generate_query_optimized(user_question, session_id, question)

        try:
            try:
                response_dict = json.loads(query_response)
            except json.JSONDecodeError:
                try:
                    # Clean up the response string before parsing
                    cleaned_response = (
                        query_response
                        .replace("'", '"')  # Replace single quotes with double quotes
                        .replace('\n', '')  # Remove newlines
                    )
                    # Try parsing again
                    response_dict = json.loads(cleaned_response)
                except json.JSONDecodeError:
                    try:
                        # As a last resort, try literal eval
                        response_dict = ast.literal_eval(query_response)
                    except (ValueError, SyntaxError):
                        raise ValueError("Could not parse response as JSON or Python dict")

            # Validate response format
            required_fields = [
                "text_explanation",
                "query_generation_status",
                "query"
            ]

            # Check if the response dictionary contains all required fields
            if not isinstance(response_dict, dict) or not all(
                    key in response_dict for key in required_fields):
                raise ValueError("Invalid response format")

            # Initialize the result
            result = {
                "text_explanation": response_dict["text_explanation"],
                "query_generation_status": response_dict["query_generation_status"],
                "query": response_dict["query"],
                "data": None,
                "html_table_data": ""
            }

            # Execute the query if status is "Yes"
            if response_dict["query_generation_status"].lower() == "yes" and response_dict["query"]:
                query_result = execute_cypher_query(driver, response_dict["query"])

                if not query_result:
                    result["text_explanation"] = generate_answer_rejection(user_question, question)

                else:
                    # Ensure the entire result is JSON serializable
                    result["data"] = json.loads(json.dumps(query_result, default=str))

                    # Generate HTML table from the data
                    result["html_table_data"] = convert_to_html_table(query_result)

                    # Save HTML table if it exists
                    if result["html_table_data"]:
                        try:
                            table_filename = f'table_{session_id}_{timestamp}.html'  # Generate a unique filename
                            file_path = STATIC_DIR / table_filename  # Set the file path

                            # Write the file
                            with open(file_path, 'w', encoding='utf-8') as f:  # Open the file in write mode
                                f.write(result["html_table_data"])  # Write the HTML table data to the file

                            # Set the correct URL using the base URL from environment
                            base_url = os.getenv('API_BASE_URL', 'http://localhost:8000')
                            result["table_file_url"] = f"{base_url}/static/temp/{table_filename}"

                        except Exception as e:  # Handle any exceptions
                            print(f"Error saving table file: {str(e)}")

                    if result["query_generation_status"] == "Yes":  # Check if the HTML table data exists
                        result["table_accept_status"] = generate_table_analysis(result["data"][:20])

                    if result["html_table_data"] and result["table_accept_status"].lower() == "yes":
                        result["table_insights"] = generate_html_table_analysis(result["data"][:20], user_question, deployment, question)

            chat_histories[session_id]["answers"].append(query_response)

            # Return the response as a JSON object
            return JSONResponse(content={
                "session_id": session_id,
                "result": result
            })
        # Handle any exceptions
        except Exception as e:
            return JSONResponse(
                content={
                    "error": f"Error processing response: {str(e)}",
                    "raw_response": query_response
                },
                status_code=500
            )
    # Handle any exceptions
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return JSONResponse(
            content={
                "error": "An error occurred processing your request",
                # Error message and line number
                "detail": str(e) + f" (Line {e.__traceback__.tb_lineno})"
            },
            status_code=500
        )

# Cache cleanup function
def cleanup_old_cache(max_age: int = 3600):
    """Remove cache entries older than max_age seconds"""
    current_time = time.time()
    for key in list(question_cache.keys()):
        if current_time - question_cache[key].get('timestamp', 0) > max_age:
            del question_cache[key]

# Add new route definitions after the existing start_session route
@router.get("/check_session/{session_id}")
async def check_session(session_id: str):
    """Check if a session exists and return its validity status"""
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
    """Get chat history for a specific session"""
    if session_id not in chat_histories:
        return JSONResponse(
            content={"error": "Session not found"},
            status_code=404
        )
    
    # Format chat history into message format
    history = []
    questions = chat_histories[session_id]["questions"]
    answers = chat_histories[session_id]["answers"]
    
    for i in range(len(questions)):
        # Add user message
        history.append({
            "sender": "user",
            "text": questions[i],
            "time": datetime.now().strftime("%I:%M %p")  # You might want to store actual timestamps in your chat_histories
        })
        
        # Add bot message if available
        if i < len(answers):
            try:
                # Parse the answer from JSON string if needed
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
    """End a session and clean up its resources"""
    if session_id in chat_histories:
        del chat_histories[session_id]
        return JSONResponse(content={"message": "Session terminated successfully"})
    return JSONResponse(
        content={"error": "Session not found"},
        status_code=404
    )