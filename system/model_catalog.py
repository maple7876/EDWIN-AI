"""EDWIN-owned identifiers and verified Ollama provider metadata."""

# Sizes are provider-published Ollama download sizes as verified 2026-07-29.
# Memory suitability is an EDWIN policy based on the published model footprint,
# not a claim of a vendor hardware requirement.
MODELS = [
    {
        "model_id": "edwin.llama.fast.v1", "catalog_version": 1,
        "display_name": "Llama 3.2 3B", "family": "llama", "family_version": "3.2",
        "parameter_count_billions": 3.21, "provider": "ollama", "provider_model": "llama3.2:latest",
        "download_size_bytes": 2_000_000_000, "license": "Llama 3.2 Community License Agreement",
        "tier": "fast", "priority": 1,
    },
    {
        "model_id": "edwin.llama.balanced.v1", "catalog_version": 1,
        "display_name": "Llama 3.1 8B", "family": "llama", "family_version": "3.1",
        "parameter_count_billions": 8, "provider": "ollama", "provider_model": "llama3.1:8b",
        "download_size_bytes": 4_900_000_000, "license": "Llama 3.1 Community License Agreement",
        "tier": "balanced", "priority": 2,
    },
    {
        "model_id": "edwin.llama.smart.v1", "catalog_version": 1,
        "display_name": "Llama 3.3 70B", "family": "llama", "family_version": "3.3",
        "parameter_count_billions": 70, "provider": "ollama", "provider_model": "llama3.3:70b",
        "download_size_bytes": 43_000_000_000, "license": "Llama 3.3 Community License Agreement",
        "tier": "smart", "priority": 3,
    },
]


def get_model(model_id: str):
    return next((model for model in MODELS if model["model_id"] == model_id), None)
