"""Detect the required local Ollama runtime without installing it."""

from __future__ import annotations

import shutil
import subprocess
from typing import Any

import requests


OLLAMA_URL = "http://127.0.0.1:11434"


def detect_runtime() -> dict[str, Any]:
    executable = shutil.which("ollama")
    version = None
    if executable:
        try:
            result = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=5)
            version = (result.stdout or result.stderr).strip() or None
        except (OSError, subprocess.SubprocessError):
            pass
    reachable = False
    models: list[dict[str, Any]] = []
    if executable:
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
            response.raise_for_status()
            reachable = True
            models = response.json().get("models", [])
        except requests.RequestException:
            pass
    if not executable:
        status, error = "not_installed", runtime_error("RUNTIME_NOT_INSTALLED", "Ollama is not installed or is not on PATH.", False)
    elif not reachable:
        status, error = "not_running", runtime_error("RUNTIME_NOT_RUNNING", "Ollama is installed but its local service is unavailable.", True)
    else:
        status, error = "available", None
    return {
        "provider": "ollama", "required": True,
        "executable": {"command": "ollama", "found": bool(executable), "resolved_path": executable, "version": version},
        "service": {"expected_base_url": OLLAMA_URL, "reachable": reachable},
        "capability": {"can_list_models": reachable, "can_pull_models": reachable, "can_generate": reachable},
        "status": status, "models": models, "error": error,
    }


def runtime_error(code: str, message: str, retryable: bool, detail: str | None = None) -> dict[str, Any]:
    return {"code": code, "message": message, "detail": detail, "retryable": retryable}
