import os
import json

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "TOKEN": "YOUR_TOKEN",
    "CHANNELS": [
        {"name": "Main Chat", "id": "1339547962723926048"}
    ],
    "YOUR_USERID": "USERID"
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        print(f"Created default configuration file: {CONFIG_FILE}")
        return DEFAULT_CONFIG
    else:
        with open(CONFIG_FILE, "r") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                print("Error reading config file; using default values.")
                config = DEFAULT_CONFIG
        return config
