from jarvis_state import context
from ddgs import DDGS


def search_web(query):

    context.set_topic(query)

    try:

        results = DDGS().text(query, max_results=5)

        output = []

        for result in results:

            title = result.get("title", "")
            body = result.get("body", "")

            output.append(
                f"{title}\n{body}"
            )

        if output:
            return "\n\n".join(output)

        return "No results found, sir."

    except Exception as e:

        return f"Internet error: {e}"
