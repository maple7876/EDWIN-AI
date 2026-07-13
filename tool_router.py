import json
from tools import open_youtube, open_google, get_time
from tool_schema import TOOLS_SCHEMA

AVAILABLE_TOOLS = {
    "youtube": open_youtube,
    "google": open_google,
    "time": get_time
}


def decide_tool(user_input, llm):
    """
    Ask LLM to decide whether a tool is needed.
    """

    prompt = f"""
You are a tool selection system.

Available tools:
{json.dumps(TOOLS_SCHEMA, indent=2)}

User input:
{user_input}

Rules:
- If a tool is needed, respond ONLY in JSON:
  {{ "tool": "...", "input": "..." }}

- If no tool is needed, respond:
  {{ "tool": null }}

Do not explain anything.
"""

    response = llm(prompt)

    try:
        return json.loads(response)
    except:
        return {"tool": None}
