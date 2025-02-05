from fastapi import APIRouter, Query
import openai
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()  # Load API keys from .env file

router = APIRouter()

# OpenAI API Configuration
openai.api_key = os.getenv("OPENAI_API_KEY")

# Neo4j AuraDB Configuration
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

class Neo4jChatbot:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query_neo4j(self, user_query):
        with self.driver.session() as session:
            response = session.run(
                """
                MATCH (a:Area)-[:HAS_PLACE]->(p:Place)
                WHERE a.name CONTAINS $query OR p.name CONTAINS $query
                RETURN a.name AS area, p.name AS place
                LIMIT 5
                """, query=user_query)
            return [record for record in response]

chatbot = Neo4jChatbot(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

@router.get("/chatbot")
def ask_chatbot(query: str = Query(..., description="Ask Tour Mate a question")):
    
    # Step 1: Process User Query using OpenAI
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5",
        messages=[{"role": "system", "content": "You are a travel guide assistant for Sri Lanka."},
                  {"role": "user", "content": query}]
    )
    ai_response = openai_response["choices"][0]["message"]["content"]

    # Step 2: Query Neo4j AuraDB for relevant places
    results = chatbot.query_neo4j(query)
    places_info = [f"Area: {record['area']}, Place: {record['place']}" for record in results]

    # Step 3: Return combined response
    return {
        "AI Response": ai_response,
        "Places Recommended": places_info if places_info else "No specific places found."
    }
