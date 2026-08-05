"""Versioned persistent-state schema for EDWIN Alpha."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any


CURRENT_SCHEMA_VERSION = 1
SETUP_STATUSES = {"not_started", "detecting_system", "choose_model", "downloading", "verifying", "completed", "failed"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_state(app_version: str = "0.1.0") -> dict[str, Any]:
    return {
        "schema_version": CURRENT_SCHEMA_VERSION,
        "app": {"product_name": "EDWIN Alpha", "app_version": app_version},
        "setup": {
            "status": "not_started", "current_step": "not_started",
            "selected_model_id": None, "installation_id": None,
            "last_error": None, "completed_at": None,
        },
        "runtime": {
            "provider": "ollama", "required": True, "status": "unknown",
            "version": None, "detected_at": None,
        },
        "models": {"installed": [], "active_model_id": None},
        "migration": {"migrated_from_legacy_state": False, "last_migrated_at": None},
    }


def validate_state(state: dict[str, Any]) -> dict[str, Any]:
    if state.get("schema_version") != CURRENT_SCHEMA_VERSION:
        raise ValueError("Unsupported EDWIN state schema")
    if state.get("setup", {}).get("status") not in SETUP_STATUSES:
        raise ValueError("Invalid EDWIN setup status")
    return state


def copy_state(state: dict[str, Any]) -> dict[str, Any]:
    return deepcopy(state)
