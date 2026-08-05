"""Platform-aware locations for EDWIN's user-owned persistent data."""

from __future__ import annotations

import os
import platform
from pathlib import Path


APP_NAME = "EDWIN Alpha"


def app_data_dir() -> Path:
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library" / "Application Support" / APP_NAME
    if system == "Windows":
        return Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / APP_NAME
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "edwin-alpha"


def state_file() -> Path:
    return app_data_dir() / "state" / "app_state.json"


def memory_dir() -> Path:
    return app_data_dir() / "memory"


def logs_dir() -> Path:
    return app_data_dir() / "logs"


def ensure_app_directories() -> None:
    for directory in (state_file().parent, memory_dir(), logs_dir()):
        directory.mkdir(parents=True, exist_ok=True)
