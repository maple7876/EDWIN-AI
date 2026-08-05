from system.app_state import load_state
from system.model_catalog import get_model


def get_selected_model() -> str:
    """
    Return the model currently selected for EDWIN.

    Raises an error if onboarding has not been completed.
    """

    state = load_state()

    selected_model = state.get("models", {}).get("active_model_id")

    if not selected_model:
        raise RuntimeError(
            "No model has been selected. Complete onboarding first."
        )

    model = get_model(selected_model)
    if not model:
        raise RuntimeError("The selected EDWIN model is no longer in the catalog.")
    return model["provider_model"]
