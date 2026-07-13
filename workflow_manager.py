ACTIVE_TASK = None


def handle_workflow(user_input):

    global ACTIVE_TASK

    text = user_input.lower()

    # -------------------------------------------------
    # MOVIE BOOKING WORKFLOW
    # -------------------------------------------------
    if "movie ticket" in text or "book movie" in text:

        ACTIVE_TASK = {
            "type": "movie_booking",
            "movie": None,
            "date": None,
            "location": None
        }

        return "Certainly, sir. Which movie would you like to see?"

    # -------------------------------------------------
    # CONTINUE ACTIVE WORKFLOW
    # -------------------------------------------------
    if ACTIVE_TASK:

        if ACTIVE_TASK["type"] == "movie_booking":

            # MOVIE
            if ACTIVE_TASK["movie"] is None:

                ACTIVE_TASK["movie"] = user_input

                return "Understood. What day would you like to book for?"

            # DATE
            elif ACTIVE_TASK["date"] is None:

                ACTIVE_TASK["date"] = user_input

                return "And which location or theater area, sir?"

            # LOCATION
            elif ACTIVE_TASK["location"] is None:

                ACTIVE_TASK["location"] = user_input

                movie = ACTIVE_TASK["movie"]
                date = ACTIVE_TASK["date"]
                location = ACTIVE_TASK["location"]

                ACTIVE_TASK = None

                return (
                    f"Searching showtimes for {movie} "
                    f"in {location} for {date}, sir."
                )

    return None
