"""Migrate legacy repository state without deleting it."""

from __future__ import annotations

import json
from pathlib import Path

from system.model_catalog import MODELS
from system.state_schema import default_state, utc_now


LEGACY_STATE_FILE = Path(__file__).parent.parent / "STATE" / "app_state.json"


def migrate_legacy_state() -> dict | None:
    if not LEGACY_STATE_FILE.exists():
        return None

    try:
        legacy = json.loads(LEGACY_STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    state = default_state()

    selected_provider_model = legacy.get("selected_model")
    legacy_installed = legacy.get("installed_models", [])

    state["migration"] = {
        "migrated_from_legacy_state": True,
        "last_migrated_at": utc_now(),
    }

    # Convert the old provider model name into EDWIN's internal model ID.
    selected_model = next(
        (
            model
            for model in MODELS
            if model["provider_model"] == selected_provider_model
        ),
        None,
    )

    if selected_model:
        state["setup"]["selected_model_id"] = selected_model["model_id"]

    # Preserve legacy installed models, but deduplicate them.
    installed_models = []
    seen_provider_models = set()

    for provider_model in legacy_installed:
        if not isinstance(provider_model, str):
            continue

        if provider_model in seen_provider_models:
            continue

        seen_provider_models.add(provider_model)

        catalog_model = next(
            (
                model
                for model in MODELS
                if model["provider_model"] == provider_model
            ),
            None,
        )

        installed_models.append(
            {
                "model_id": catalog_model["model_id"] if catalog_model else None,
                "provider": "ollama",
                "provider_model": provider_model,
                "installed_at": None,
                "verified_at": None,
                "provider_reported_size_bytes": None,
            }
        )

    state["models"]["installed"] = installed_models

    # A migrated model must still be verified by the new setup system.
    if selected_model:
        state["setup"].update(
            {
                "status": "verifying",
                "current_step": "verifying",
            }
        )
    else:
        state["setup"].update(
            {
                "status": "choose_model",
                "current_step": "choose_model",
            }
        )

    return state