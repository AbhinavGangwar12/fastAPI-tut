import json
from pathlib import Path

DB_FILE = Path("patients.json")


def get_info():
    if not DB_FILE.exists():
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)
