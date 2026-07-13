from browser_agent import browser_search, open_website


def handle_internet_request(user_input):

    text = user_input.lower().strip()

    # -------------------------------------------------
    # MANUAL WEBSITE OPENING
    # -------------------------------------------------
    if text.startswith("open ") or text.startswith("go to "):

        website = (
            text.replace("open ", "")
            .replace("go to ", "")
            .strip()
        )

        return open_website(website)

    # -------------------------------------------------
    # LIVE WEB QUESTIONS
    # -------------------------------------------------
    web_keywords = [
        "search",
        "look up",
        "find",
        "who is",
        "what is",
        "latest",
        "news",
        "showtimes",
        "weather",
        "price"
    ]

    if any(keyword in text for keyword in web_keywords):

        results = browser_search(user_input)

        return (
            "Live internet data retrieved successfully.\n\n"
            + results[:1500]
        )

    return None
