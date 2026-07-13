from memory_bridge import ollama_llm
import json


def create_plan(user_input):

    prompt = f"""
You are an AI planning system.

Break the user's request into steps.

Return ONLY JSON.

Example:

[
  "step 1",
  "step 2",
  "step 3"
]

User:
{user_input}
"""

    response = ollama_llm(prompt)

    try:
        return json.loads(response)

    except:
        return []
