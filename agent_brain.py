from memory_bridge import ollama_llm
import json


def decide_action(user_input, model="qwen2.5"):

    text = user_input.lower().strip()

    # -----------------------------
    # TOOL DETECTION
    # -----------------------------
    if "youtube" in text:

        if "search" in text:
            return {
                "action": "tool",
                "tool_name": "youtube_search",
                "tool_input": text.replace("youtube search", "").strip()
            }

        return {
            "action": "tool",
            "tool_name": "open_youtube",
            "tool_input": ""
        }

    if "google" in text:
        return {
            "action": "tool",
            "tool_name": "open_google",
            "tool_input": ""
        }

    if (
        text == "time"
        or "what time" in text
        or "current time" in text
    ):
        return {
            "action": "tool",
            "tool_name": "time",
            "tool_input": ""
        }

    # -----------------------------
    # WORKFLOW DETECTION
    # -----------------------------
    workflow_keywords = [
        "book",
        "reserve",
        "schedule",
        "plan",
        "movie tickets",
        "flight",
        "hotel"
    ]

    if any(word in text for word in workflow_keywords):
        return {
            "action": "workflow",
            "tool_name": "",
            "tool_input": user_input
        }

    # -----------------------------
    # IDENTITY / CONVERSATION
    # -----------------------------
    identity_keywords = [
        "your name",
        "who are you",
        "are you jarvis",
        "are you edwin",
        "what are you",
        "who made you",
        "what can you do"
    ]

    if any(keyword in text for keyword in identity_keywords):
        return {
            "action": "respond",
            "tool_name": "",
            "tool_input": user_input
        }

    # -----------------------------
    # INTERNET DETECTION
    # -----------------------------
    internet_keywords = [
        "search",
        "what is",
        "who is",
        "tell me about",
        "latest",
        "news",
        "find",
        "lookup",
        "information on"
    ]

    if any(word in text for word in internet_keywords):
        return {
            "action": "internet",
            "tool_name": "",
            "tool_input": user_input
        }

    # -----------------------------
    # LLM FALLBACK
    # -----------------------------
    prompt = f"""
You are the decision engine for EDWIN, an advanced personal AI assistant.

Choose ONE action:

respond
tool
internet
workflow

Return ONLY JSON.

User:
{user_input}
"""

    response = ollama_llm(prompt, model=model)

    try:
        return json.loads(response)

    except:
        return {
            "action": "respond",
            "tool_name": "",
            "tool_input": user_input
        }
