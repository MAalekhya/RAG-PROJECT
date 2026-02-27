from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# Add src to Python path for service import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.services.gemini_service import GeminiService

app = FastAPI(title="Gemini Chat API")

# Initialize GeminiService
try:
    gemini_service = GeminiService()
except ValueError as e:
    # This will fail if GOOGLE_API_KEY is not set
    # We'll handle this gracefully during runtime if needed
    gemini_service = None
    print(f"Warning: GeminiService initialization failed: {e}")

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not gemini_service:
        raise HTTPException(status_code=500, detail="GeminiService not initialized. Check API key.")
    
    try:
        print("calling gemini service from backend")
        response_text = gemini_service.chat(request.prompt)
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Gemini Chat API"}

@app.get("/serverinfo")
async def server_info():
    return {"status": "serverinfo", "info": "This backend is manufacturing chatbot"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
