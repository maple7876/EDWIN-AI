from datetime import datetime
import os
from tool_registry import TOOLS

def process_command(user_input):

    text = user_input.lower().strip()

    # -----------------------------
    # TIME
    # -----------------------------
    if text in ["time", "what time is it", "current time"]:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}, sir."

    # -----------------------------
    # DATE
    # -----------------------------
    if text in ["date", "what is the date", "today's date"]:
        current_date = datetime.now().strftime("%B %d, %Y")
        return f"Today's date is {current_date}, sir."

    # -----------------------------
    # STATUS
    # -----------------------------
    if text in ["status", "status report", "system status"]:
        return (
            "All systems operational, sir. "
            "Memory systems active. "
            "Model routing online."
        )

    # -----------------------------
    # CLEAR TERMINAL
    # -----------------------------
    if text == "clear":
        os.system("clear")
        return "Terminal cleared."

    # -----------------------------
    # HELP
    # -----------------------------
    if text == "help":
        return (
            "Available commands: "
            "time, date, status, clear, help."
        )
    # -----------------------------
    # TOOL EXECUTION
    # -----------------------------
    for tool_name, tool_data in TOOLS.items():

        if f"open {tool_name}" in text:

            tool_function = tool_data["function"]

            return tool_function()

    return None
