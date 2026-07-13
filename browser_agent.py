import requests
from playwright.sync_api import sync_playwright


# -------------------------------------------------
# SILENT INTERNET SEARCH
# -------------------------------------------------
def browser_search(query):

    try:

        url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + query.replace(" ", "_")
        )

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Macintosh; Intel Mac OS X 10_15_7)"
            )
        }

        response = requests.get(
            url,
            headers=headers
        )

        # DEBUG
        print("\n[INTERNET STATUS]")
        print("STATUS:", response.status_code)
        print()

        data = response.json()

        if "extract" in data:
            return data["extract"]

        if "detail" in data:
            return data["detail"]

        return "No useful information found, sir."

    except Exception as e:

        return f"Internet retrieval error: {e}"


# -------------------------------------------------
# VISIBLE BROWSER MODE
# -------------------------------------------------
def open_website(url):

    if not url.startswith("http"):
        url = "https://" + url

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        page.goto(url)

        input("Press ENTER to close browser...")

        browser.close()

        return f"Opening {url}, sir."
