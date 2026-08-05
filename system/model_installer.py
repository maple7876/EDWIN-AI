"""Managed, observable Ollama model installation."""

from __future__ import annotations

import re
import subprocess
import threading
import uuid
from datetime import datetime, timezone
from typing import Any, Callable

from system.runtime_detector import detect_runtime


PERCENTAGE = re.compile(r"(\d{1,3})%")


def is_model_installed(provider_model: str) -> bool:
    runtime = detect_runtime()
    return any(item.get("name") == provider_model for item in runtime.get("models", []))


class ModelInstallJob:
    def __init__(self, provider_model: str, on_update: Callable[[dict[str, Any]], None]):
        self.installation_id = str(uuid.uuid4())
        self.provider_model = provider_model
        self.on_update = on_update
        self.status: dict[str, Any] = {"installation_id": self.installation_id, "model_id": None, "status": "queued", "phase": "queued", "progress": {"percent": None, "downloaded_bytes": None, "total_bytes": None, "indeterminate": True}, "message": "Waiting to download model", "error": None, "started_at": None, "updated_at": None}

    def _publish(self, **updates: Any) -> None:
        self.status.update(updates)
        self.status["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.on_update(self.status.copy())

    def start(self) -> None:
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self) -> None:
        if is_model_installed(self.provider_model):
            self._publish(status="complete", phase="complete", message="Model is already present")
            return
        self._publish(status="running", phase="downloading", message="Downloading model", started_at=datetime.now(timezone.utc).isoformat())
        try:
            process = subprocess.Popen(["ollama", "pull", self.provider_model], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            assert process.stdout is not None
            for line in process.stdout:
                match = PERCENTAGE.search(line)
                progress = self.status["progress"].copy()
                if match:
                    progress.update({"percent": min(100, int(match.group(1))), "indeterminate": False})
                self._publish(progress=progress, message=line.strip() or "Downloading model")
            if process.wait() != 0:
                raise RuntimeError("Ollama reported that the model download failed")
            self._publish(status="complete", phase="complete", progress={"percent": 100, "downloaded_bytes": None, "total_bytes": None, "indeterminate": False}, message="Model download complete")
        except (OSError, RuntimeError) as error:
            self._publish(status="failed", phase="failed", message="Model download failed", error={"code": "MODEL_DOWNLOAD_FAILED", "message": str(error), "detail": None, "retryable": True})
