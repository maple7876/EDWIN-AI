def format_response(response):

    replacements = {
        "Is there anything specific you need assistance with, sir?": "",
        "How may I assist you further?": "",
        "How may I assist you, sir?": "",
        "How may I assist you today?": "",
        "How can I assist you today?": "",
        "Would you like to know more?": "",
        "Would you like to explore further?": "",
        "Based on your previous statement,": "",
        "Certainly, sir.": "",
        "Affirmative, sir.": "",
        "Is there anything specific you need assistance with, sir?": "",
        "How may I assist you further?": "",
        "How may I assist you, sir?": "",
    }

    for old, new in replacements.items():
        response = response.replace(old, new)

    # cleanup spacing
    response = " ".join(response.split())

    return response.strip()
