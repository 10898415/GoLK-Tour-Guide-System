from fastapi import FastAPI
from fastapi.responses import FileResponse
from routers import chatbot

app = FastAPI(title="GoLK - AI Tour Guide")

# Include chatbot routes
app.include_router(chatbot.router, prefix="/api", tags=["Chatbot"])

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/")
def home():
    return {"message": "Welcome to GoLK - Your AI-Powered Sri Lanka Tour Guide!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)