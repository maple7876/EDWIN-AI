"""Verify an installed model via Ollama's actual inference endpoint."""

from __future__ import annotations

import requests

from system.model_installer import is_model_installed
from system.runtime_detector import OLLAMA_URL


def verify_model(provider_model: str) -> tuple[bool, dict | None]:
    if not is_model_installed(provider_model):
        return False, {"code": "MODEL_NOT_FOUND_AFTER_INSTALL", "message": "Ollama does not report the selected model as installed.", "detail": None, "retryable": True}
    try:
        response = requests.post(f"{OLLAMA_URL}/api/generate", json={"model": provider_model, "prompt": "Reply with OK.", "stream": False, "options": {"num_predict": 8}}, timeout=90)
        response.raise_for_status()
        if not response.json().get("response", "").strip():
            raise RuntimeError("The model returned an empty verification response")
    except (requests.RequestException, RuntimeError) as error:
        return False, {"code": "MODEL_VERIFICATION_FAILED", "message": "EDWIN could not verify the selected model.", "detail": str(error), "retryable": True}
    return True, None
