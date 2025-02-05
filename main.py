from fastapi import FastAPI
from routers import chatbot

app = FastAPI(title="GoLK - AI Tour Guide")

# Include Routers
app.include_router(chatbot.router, prefix="/api", tags=["Chatbot"])

@app.get("/")
def home():
    return {"message": "Welcome to GoLK - Your AI-Powered Sri Lanka Tour Guide!"}
