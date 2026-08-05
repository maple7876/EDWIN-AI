import json
import os


CONFIG_FILE = "STATE/model_config.json"


def save_selected_model(model_name: str):
    os.makedirs("STATE", exist_ok=True)

    data = {
        "model": model_name
    }

    with open(CONFIG_FILE, "w") as file:
        json.dump(data, file, indent=4)


    return {
        "status": "saved",
        "model": model_name
    }



def get_selected_model():

    if not os.path.exists(CONFIG_FILE):
        return {
            "model": None
        }


    with open(CONFIG_FILE, "r") as file:
        return json.load(file)