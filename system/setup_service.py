"""Authoritative setup state machine for first-launch onboarding."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from system.app_state import load_state, save_state
from system.hardware_detector import compatibility_for, detect_system, recommend_models
from system.model_catalog import get_model
from system.model_installer import ModelInstallJob, is_model_installed
from system.model_verifier import verify_model
from system.runtime_detector import detect_runtime


class SetupService:
    def __init__(self) -> None:
        self.job: ModelInstallJob | None = None
        self._reconcile_interrupted_setup()

    def _save(self, state: dict[str, Any]) -> None:
        save_state(state)

    def _set_failure(self, state: dict[str, Any], error: dict[str, Any]) -> None:
        state["setup"].update({"status": "failed", "current_step": "failed", "last_error": {**error, "occurred_at": datetime.now(timezone.utc).isoformat()}})
        self._save(state)

    def _reconcile_interrupted_setup(self) -> None:
        try:
            state = load_state()
        except RuntimeError:
            return
        if state["setup"]["status"] not in {"downloading", "verifying"}:
            return
        selected = get_model(state["setup"].get("selected_model_id") or "")
        if selected and is_model_installed(selected["provider_model"]):
            state["setup"].update({"status": "verifying", "current_step": "verifying", "installation_id": None})
        else:
            state["setup"].update({"status": "choose_model", "current_step": "choose_model", "installation_id": None})
        self._save(state)

    def state(self) -> dict[str, Any]:
        return load_state()

    def detect(self) -> dict[str, Any]:
        state = load_state()
        was_completed = state["setup"]["status"] == "completed"

        state["setup"].update({
            "status": "detecting_system",
            "current_step": "detecting_system",
            "last_error": None,
        })
        self._save(state)

        runtime = detect_runtime()

        state["runtime"].update({
            "status": runtime["status"],
            "version": runtime["executable"]["version"],
            "detected_at": datetime.now(timezone.utc).isoformat(),
        })

        if was_completed:
            state["setup"].update({
                "status": "completed",
                "current_step": "completed",
            })
        else:
            state["setup"].update({
                "status": "choose_model",
                "current_step": "choose_model",
            })

        self._save(state)

        recommendations = recommend_models(
            runtime["status"] == "available"
        )

        return {
            "hardware": recommendations["system"],
            "runtime": runtime,
            "models": recommendations,
            "next_state": (
                "completed" if was_completed else "choose_model"
            ),
        }
    def select_model(self, model_id: str) -> dict[str, Any]:
        state, model = load_state(), get_model(model_id)
        if not model:
            raise SetupError("MODEL_UNKNOWN", "The requested EDWIN model does not exist.", False, 422)
        runtime = detect_runtime()
        result = compatibility_for(model, detect_system(), runtime["status"] == "available")
        if result["status"] == "incompatible":
            raise SetupError("MODEL_INCOMPATIBLE", "This model is not compatible with this Mac.", False, 422, result)
        state["setup"].update({"status": "choose_model", "current_step": "choose_model", "selected_model_id": model_id, "last_error": None})
        self._save(state)
        return {"selected_model_id": model_id, "compatibility": result, "next_state": "choose_model"}

    def install(self) -> dict[str, Any]:
        state = load_state()
        if self.job and self.job.status["status"] == "running":
            raise SetupError("INSTALLATION_ALREADY_ACTIVE", "A model installation is already running.", True, 409)
        model = get_model(state["setup"].get("selected_model_id") or "")
        if not model:
            raise SetupError("MODEL_UNKNOWN", "Choose a model before installation.", False, 409)
        runtime = detect_runtime()
        if runtime["status"] != "available":
            raise SetupError(runtime["error"]["code"], runtime["error"]["message"], runtime["error"]["retryable"], 503)
        self.job = ModelInstallJob(model["provider_model"], self._job_update)
        self.job.status["model_id"] = model["model_id"]
        state["setup"].update({"status": "downloading", "current_step": "downloading", "installation_id": self.job.installation_id, "last_error": None})
        self._save(state)
        self.job.start()
        return {"installation": self.job.status, "next_state": "downloading"}

    def _job_update(self, job_status: dict[str, Any]) -> None:
        if job_status["status"] == "failed":
            self._set_failure(load_state(), job_status["error"])

    def install_status(self) -> dict[str, Any]:
        state = load_state()
        if not self.job:
            return {"installation": None, "setup_status": state["setup"]["status"]}
        if self.job.status["status"] == "complete" and state["setup"]["status"] == "downloading":
            state["setup"].update({"status": "verifying", "current_step": "verifying"})
            self._save(state)
        return {"installation": self.job.status, "setup_status": load_state()["setup"]["status"]}

    def verify(self) -> dict[str, Any]:
        state = load_state()
        model = get_model(state["setup"].get("selected_model_id") or "")
        if not model:
            raise SetupError("MODEL_UNKNOWN", "No model is selected.", False, 409)
        state["setup"].update({"status": "verifying", "current_step": "verifying"})
        self._save(state)
        success, error = verify_model(model["provider_model"])
        if not success:
            self._set_failure(state, error)
            raise SetupError(error["code"], error["message"], error["retryable"], 422, error)
        now = datetime.now(timezone.utc).isoformat()
        installed = [item for item in state["models"]["installed"] if item.get("model_id") != model["model_id"]]
        installed.append({"model_id": model["model_id"], "provider": "ollama", "provider_model": model["provider_model"], "installed_at": now, "verified_at": now, "provider_reported_size_bytes": model["download_size_bytes"]})
        state["models"].update({"installed": installed, "active_model_id": model["model_id"]})
        state["setup"].update({"status": "completed", "current_step": "completed", "completed_at": now, "last_error": None, "installation_id": None})
        self._save(state)
        return {"verified": True, "next_state": "completed", "state": state}

    def retry(self, operation: str) -> dict[str, Any]:
        if operation == "detect": return self.detect()
        if operation == "install": return self.install()
        if operation == "verify": return self.verify()
        raise SetupError("INVALID_SETUP_TRANSITION", "Unknown setup retry operation.", False, 422)


class SetupError(Exception):
    def __init__(self, code: str, message: str, retryable: bool, status_code: int, detail: Any = None):
        self.error = {"code": code, "message": message, "detail": detail, "retryable": retryable}
        self.status_code = status_code
        super().__init__(message)
