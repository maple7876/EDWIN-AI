"""macOS Apple Silicon hardware inventory and backend-owned compatibility."""

from __future__ import annotations

import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import psutil

from system.model_catalog import MODELS


GIB = 1024 ** 3


def _sysctl(name: str) -> str | None:
    try:
        result = subprocess.run(["sysctl", "-n", name], capture_output=True, text=True, timeout=2)
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def detect_system() -> dict[str, Any]:
    total_memory = psutil.virtual_memory().total
    machine = platform.machine().lower()
    apple_silicon = platform.system() == "Darwin" and machine in {"arm64", "aarch64"}
    chip = _sysctl("machdep.cpu.brand_string") if platform.system() == "Darwin" else platform.processor()
    storage = shutil.disk_usage(str(Path.home()))
    return {
        "detected_at": datetime.now(timezone.utc).isoformat(),
        "operating_system": {"family": "macos" if platform.system() == "Darwin" else "unknown", "name": platform.system(), "version": platform.mac_ver()[0] or platform.version()},
        "architecture": {"machine": machine, "process_bits": 64, "is_apple_silicon": apple_silicon},
        "cpu": {"model": chip or None, "physical_cores": psutil.cpu_count(logical=False), "logical_cores": psutil.cpu_count(logical=True)},
        "memory": {"total_bytes": total_memory, "total_gib": round(total_memory / GIB, 1), "unified_memory": {"applicable": apple_silicon, "total_bytes": total_memory if apple_silicon else None, "total_gib": round(total_memory / GIB, 1) if apple_silicon else None}},
        "gpu": {"detected": apple_silicon, "devices": ([{"vendor": "Apple", "model": chip or "Apple Silicon", "memory_bytes": total_memory, "memory_gib": round(total_memory / GIB, 1), "memory_type": "unified"}] if apple_silicon else [])},
        "storage": {"model_storage_path": str(Path.home()), "available_bytes": storage.free, "available_gib": round(storage.free / GIB, 1)},
    }


def compatibility_for(model: dict[str, Any], hardware: dict[str, Any], runtime_available: bool) -> dict[str, Any]:
    # Conservative EDWIN policy: require published download size on disk and
    # enough unified memory for model weights; recommend 1.5x the footprint.
    size = model["download_size_bytes"]
    memory = hardware["memory"]["total_bytes"]
    disk = hardware["storage"]["available_bytes"]
    architecture_ok = hardware["architecture"]["is_apple_silicon"]
    disk_ok, memory_ok = disk >= size, memory >= size
    checks = {"runtime_available": runtime_available, "operating_system_supported": hardware["operating_system"]["family"] == "macos", "architecture_supported": architecture_ok, "memory_sufficient": memory_ok, "disk_sufficient": disk_ok, "gpu_requirement_satisfied": architecture_ok}
    reasons = []
    if not checks["operating_system_supported"]: reasons.append({"code": "UNSUPPORTED_OS", "message": "Milestone 1 supports macOS only."})
    if not architecture_ok: reasons.append({"code": "UNSUPPORTED_ARCHITECTURE", "message": "Milestone 1 supports Apple Silicon only."})
    if not disk_ok: reasons.append({"code": "INSUFFICIENT_DISK_SPACE", "message": "Insufficient available disk space for this model download."})
    if not memory_ok: reasons.append({"code": "INSUFFICIENT_MEMORY", "message": "This model's published footprint exceeds available unified memory."})
    if not runtime_available: reasons.append({"code": "RUNTIME_UNAVAILABLE", "message": "Ollama must be available before installation."})
    impossible = not all(checks[key] for key in ("operating_system_supported", "architecture_supported", "memory_sufficient", "disk_sufficient"))
    if impossible: status = "incompatible"
    elif memory >= int(size * 1.5) and disk >= int(size * 1.25): status = "recommended"
    elif memory >= size and disk >= size: status = "compatible"
    else: status = "not_recommended"
    return {"model_id": model["model_id"], "status": status, "recommended_tier": model["tier"], "checks": checks, "reasons": reasons, "estimated": {"download_size_bytes": size, "required_available_disk_bytes": size}}


def recommend_models(runtime_available: bool = False) -> dict[str, Any]:
    hardware = detect_system()
    return {"system": hardware, "catalog_version": 1, "choices": [{**model, "compatibility": compatibility_for(model, hardware, runtime_available)} for model in MODELS]}
