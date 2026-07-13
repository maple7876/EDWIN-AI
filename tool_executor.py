from tools import open_youtube, open_google, get_time


def execute_tool(tool_name, tool_input=None):

    tool_name = (tool_name or "").lower().strip()

    tools = {
        "youtube": open_youtube,
        "open_youtube": open_youtube,
        "google": open_google,
        "open_google": open_google,
        "time": get_time,
        "get_time": get_time
    }

    if tool_name in tools:
        return tools[tool_name]()

    return f"Tool not found: {tool_name}"
