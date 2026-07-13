from config import SYSTEM_MODE

PROFILE_MEMORY = {
    "favorite_aircraft": None,
    "favorite_car": None,
    "favorite_color": None,
    "main_project": None,
    "goal": None
}

SHOWCASE_PROFILE = {
    "favorite_aircraft": "SR-71 Blackbird",
    "favorite_car": "Audi R8",
    "main_project": "J.A.R.V.I.S. AI System",
    "goal": "Build next-generation technology systems"
}


def update_profile_memory(user_input):

    text = user_input.lower()

    # Favorite aircraft
    if "favorite aircraft is" in text:
        PROFILE_MEMORY["favorite_aircraft"] = user_input.split("is")[-1].strip()

    # Favorite car
    if "favorite car is" in text:
        PROFILE_MEMORY["favorite_car"] = user_input.split("is")[-1].strip()

    # Favorite color
    if "favorite color is" in text:
        PROFILE_MEMORY["favorite_color"] = user_input.split("is")[-1].strip()

    # Main project
    if "main project is" in text:
        PROFILE_MEMORY["main_project"] = user_input.split("is")[-1].strip()

    # Goal
    if "my goal is" in text:
        PROFILE_MEMORY["goal"] = user_input.split("is")[-1].strip()


def get_profile_context():

    lines = []

    if SYSTEM_MODE == "showcase":
        memory_source = SHOWCASE_PROFILE
    else:
        memory_source = PROFILE_MEMORY

    for key, value in memory_source.items():

        if value:
            lines.append(f"{key}: {value}")

    return "\n".join(lines)
