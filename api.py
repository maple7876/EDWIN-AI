print("\n\n========== API LOADED SUCCESSFULLY ==========\n\n")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent_controller import JarvisAgent

app = FastAPI(title="Jarvis API")

# Allow the React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "tauri://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jarvis = JarvisAgent()

@app.get("/status")
def status():
    return {
        "assistant": "Jarvis Alpha",
        "version": "0.1.0",
        "model": "Qwen 2.5",
        "connected": True,
        "memory": True,
        "internet": True
    }
class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(req: ChatRequest):
    response = jarvis.process(req.message)

    return {
        "response": response
    }