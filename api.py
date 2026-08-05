"""EDWIN Alpha local backend and first-launch setup API."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from system.hardware_detector import recommend_models
from agent_controller import JarvisAgent
from system.app_state import load_state
from system.runtime_detector import detect_runtime
from system.setup_service import SetupError, SetupService


BACKEND_STARTED_AT = datetime.now(timezone.utc).isoformat()
app = FastAPI(title="EDWIN Alpha API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "tauri://localhost"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
jarvis = JarvisAgent()
setup = SetupService()


class ChatRequest(BaseModel):
    message: str


class ModelSelectionRequest(BaseModel):
    model_id: str = Field(min_length=1)


class RetryRequest(BaseModel):
    operation: str


def setup_exception(error: SetupError) -> None:
    raise HTTPException(status_code=error.status_code, detail={"error": error.error})


@app.get("/health")
def health():
    try:
        state = load_state()
        runtime = detect_runtime()
        status = "ready" if runtime["status"] == "available" else "degraded"
        return {"status": status, "backend": {"name": "EDWINBackend", "version": "0.1.0", "started_at": BACKEND_STARTED_AT}, "state": {"readable": True, "schema_version": state["schema_version"], "setup_status": state["setup"]["status"]}, "runtime": {"provider": "ollama", "status": runtime["status"], "version": runtime["executable"]["version"]}}
    except Exception as error:
        return {"status": "error", "backend": {"name": "EDWINBackend", "version": "0.1.0", "started_at": BACKEND_STARTED_AT}, "state": {"readable": False}, "runtime": None, "error": {"code": "STATE_READ_FAILED", "message": str(error)}}


@app.get("/setup/state")
def get_setup_state():
    return {"state": setup.state()}


@app.post("/setup/detect")
def detect_setup():
    try:
        return setup.detect()
    except SetupError as error:
        setup_exception(error)


@app.post("/setup/model-selection")
def select_setup_model(request: ModelSelectionRequest):
    try:
        return setup.select_model(request.model_id)
    except SetupError as error:
        setup_exception(error)


@app.post("/setup/install")
def install_setup_model():
    try:
        return setup.install()
    except SetupError as error:
        setup_exception(error)


@app.get("/setup/install-status")
def install_setup_status():
    return setup.install_status()


@app.post("/setup/verify")
def verify_setup_model():
    try:
        return setup.verify()
    except SetupError as error:
        setup_exception(error)


@app.post("/setup/retry")
def retry_setup(request: RetryRequest):
    try:
        return setup.retry(request.operation)
    except SetupError as error:
        setup_exception(error)


# Compatibility routes retained for the existing desktop/chat surface.
@app.get("/status")
def status():
    state = setup.state()
    return {"assistant": "EDWIN Alpha", "version": "0.1.0", "model": state["models"]["active_model_id"], "connected": True, "memory": True, "internet": True}


@app.get("/hardware")
def hardware():
    runtime = detect_runtime()
    return recommend_models(runtime["status"] == "available")

@app.get("/onboarding")
def onboarding():
    state = setup.state()
    return {"complete": state["setup"]["status"] == "completed", "selected_model": state["setup"]["selected_model_id"]}


@app.get("/state")
def get_state():
    return setup.state()


@app.post("/chat")
def chat(request: ChatRequest):
    if setup.state()["setup"]["status"] != "completed":
        raise HTTPException(status_code=409, detail={"error": {"code": "SETUP_NOT_COMPLETED", "message": "Complete EDWIN setup before starting a chat.", "retryable": False}})
    return {"response": jarvis.process(request.message)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
