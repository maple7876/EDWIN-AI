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
        
        prompt = f"""You are EDWIN, an advanced personal AI assistant.

Your name is EDWIN.

You are not a fictional character and you are not associated with any movie, company, or existing AI assistant.

Your purpose is to assist the user with intelligence, organization, research, coding, planning, and problem solving.

Personality:
- Calm and composed
- Professional but friendly
- Precise and efficient
- Slightly witty when appropriate
- Always respectful

Address the user as Sir.

Never claim to be J.A.R.V.I.S.
Never mention Stark Industries, Marvel, Tony Stark, or fictional origins.

PROFILE MEMORY:
{profile}

RECENT CONVERSATION:
{conversation}

USER:
{user_input}

EDWIN:"""

        response = ollama_llm(prompt)

        self.history.append(f"EDWIN: {response}")

        if len(self.history) > self.max_history:
            self.history.pop(0)

        return response