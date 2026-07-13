from tools import open_youtube, open_google, get_time

TOOLS = {
    "youtube": {
        "function": open_youtube,
        "description": "Open YouTube in browser"
    },

    "google": {
        "function": open_google,
        "description": "Open Google in browser"
    },

    "time": {
        "function": get_time,
        "description": "Get the current time"
    }
}
