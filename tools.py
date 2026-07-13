import webbrowser
from datetime import datetime


def open_youtube():
    webbrowser.open("https://youtube.com")
    return "Opening YouTube."


def open_google():
    webbrowser.open("https://google.com")
    return "Opening Google."


def get_time():
    return f"The time is {datetime.now().strftime('%I:%M %p')}."
