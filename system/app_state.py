"""Atomic, versioned EDWIN persistent state."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from system.paths import ensure_app_directories, state_file
from system.state_migrations import migrate_legacy_state
from system.state_schema import default_state, validate_state


STATE_FILE = state_file()


def load_state() -> dict[str, Any]:
    ensure_app_directories()
    if not STATE_FILE.exists():
        save_state(migrate_legacy_state() or default_state())
    try:
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return validate_state(state)
    except (OSError, json.JSONDecodeError, ValueError):
        # Preserve a corrupt file for diagnosis instead of overwriting it.
        raise RuntimeError("EDWIN persistent state could not be read")


def save_state(state: dict[str, Any]) -> None:
    ensure_app_directories()
    validate_state(state)
    temporary = STATE_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, STATE_FILE)


def update_state(**updates: Any) -> dict[str, Any]:
    state = load_state()
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(state.get(key), dict):
            state[key].update(value)
        else:
            state[key] = value
    save_state(state)
    return state
