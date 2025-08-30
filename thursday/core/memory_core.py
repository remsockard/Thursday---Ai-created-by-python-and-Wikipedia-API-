import json
import os

FACTS_FILE = "facts.json"

def init_memory():
    if not os.path.exists(FACTS_FILE):
        with open(FACTS_FILE, "w") as f:
            json.dump({}, f)

def save_fact(key, value):
    key = key.lower()
    data = load_facts()
    data[key] = value
    with open(FACTS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_fact(key):
    key = key.lower()
    data = load_facts()
    return data.get(key)

def load_facts():
    if not os.path.exists(FACTS_FILE):
        return {}
    with open(FACTS_FILE, "r") as f:
        return json.load(f)
