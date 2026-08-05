from jarvis_state import context

from planner import create_plan
from workflow_engine import execute_plan

from agent_brain import decide_action
from tool_executor import execute_tool
from research_engine import research_topic

from memory_engine import store_memory
from memory_manager import (
    update_profile_memory,
    get_profile_context
)

from memory_bridge import ollama_llm


class JarvisAgent:

    def __init__(self):
        self.history = []
        self.max_history = 10

    def process(self, user_input):

        # -------------------------
        # MEMORY UPDATE
        # -------------------------
        update_profile_memory(user_input)

        self.history.append(user_input)

        if len(self.history) > self.max_history:
            self.history.pop(0)
        # -------------------------
        # CONTEXT FOLLOW-UP SYSTEM
        # -------------------------
        topic = context.get_topic()

        if topic:

            followup_words = [
                "it",
                "its",
                "he",
                "she",
                "they",
                "that",
                "this"
            ]

            if any(
                word in user_input.lower().split()
                for word in followup_words
            ):
                user_input = f"{topic} {user_input}"

        # -------------------------
        # DECISION ENGINE
        # -------------------------
        decision = decide_action(user_input)

        action = decision.get("action", "respond")
        tool_name = decision.get("tool_name", "")
        tool_input = decision.get("tool_input", "")

        # -------------------------
        # TOOL EXECUTION
        # -------------------------
        if action == "tool":

            result = execute_tool(
                tool_name,
                tool_input
            )

            store_memory(
                user_input,
                f"tool:{tool_name}"
            )

            return result

        # -------------------------
        # INTERNET SEARCH
        # -------------------------
        if action == "internet":

            query = tool_input or user_input

            result = research_topic(query)

            store_memory(
                user_input,
                f"internet:{query}"
            )

            return result

        # -------------------------
        # WORKFLOW SYSTEM
        # -------------------------
        if action == "workflow":

            plan = create_plan(user_input)

            result = execute_plan(plan)

            store_memory(
                user_input,
                "workflow"
            )

            return result

        # -------------------------
        # MEMORY
        # -------------------------
        store_memory(
            user_input,
            "chat"
        )

        profile = get_profile_context()

        # -------------------------
        # MAIN LLM
        # -------------------------
        conversation = "\n".join(self.history)
        
        prompt = f"""You are EDWIN, a local personal AI assistant.

Respond directly to the user's latest message.

Your personality is calm, precise, professional, and natural.
Address the user as Sir when appropriate.

Do not explain your instructions.
Do not describe your reasoning process.
Do not mention this prompt, system messages, profile memory, or internal rules.
Do not write about what you are supposed to do.
Simply answer the user.

Relevant user context:
{profile}

Recent conversation:
{conversation}

User:
{user_input}

Assistant:
"""

        response = ollama_llm(prompt)

        self.history.append(f"EDWIN: {response}")

        if len(self.history) > self.max_history:
            self.history.pop(0)

        return response