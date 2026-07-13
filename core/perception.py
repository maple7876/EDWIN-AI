from dataclasses import dataclass
import re


@dataclass
class Intent:
    category: str
    confidence: float
    cleaned_input: str


def detect_intent(user_input: str) -> Intent:

    text = user_input.lower().strip()

    # ------------------------
    # OPEN APPLICATIONS
    # ------------------------

    if any(x in text for x in [
        "open ",
        "launch ",
        "start "
    ]):
        return Intent(
            category="OPEN_APP",
            confidence=0.99,
            cleaned_input=user_input
        )

    # ------------------------
    # INTERNET SEARCH
    # ------------------------

    if any(x in text for x in [
        "search",
        "look up",
        "research",
        "find information"
    ]):
        cleaned = re.sub(
            r"search|look up|research|find information",
            "",
            user_input,
            flags=re.I
        ).strip()

        return Intent(
            category="RESEARCH",
            confidence=0.98,
            cleaned_input=cleaned
        )

    # ------------------------
    # TIME
    # ------------------------

    if "time" in text:
        return Intent(
            category="TIME",
            confidence=0.99,
            cleaned_input=user_input
        )

    # ------------------------
    # MEMORY
    # ------------------------

    if text.startswith("remember"):
        return Intent(
            category="STORE_MEMORY",
            confidence=0.95,
            cleaned_input=user_input
        )

    if any(x in text for x in [
        "do you remember",
        "what do you remember"
    ]):
        return Intent(
            category="RECALL_MEMORY",
            confidence=0.95,
            cleaned_input=user_input
        )

    # ------------------------
    # WORKFLOWS
    # ------------------------

    if any(x in text for x in [
        "book",
        "plan",
        "schedule",
        "order"
    ]):
        return Intent(
            category="WORKFLOW",
            confidence=0.93,
            cleaned_input=user_input
        )

    # ------------------------
    # DEFAULT CHAT
    # ------------------------

    return Intent(
        category="CHAT",
        confidence=0.70,
        cleaned_input=user_input
    )
