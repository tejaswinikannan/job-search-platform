from pathlib import Path
import json

DATA_DIR = Path("data")
DATA_JOBS_FILE = DATA_DIR/"jobs.json"


def load_data():
    if DATA_JOBS_FILE.exists():
        with open(DATA_JOBS_FILE, "r") as f:
            content = f.read()
            if content.strip():
                return json.loads(content).get("jobs", [])
    return []

def save_data(data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_JOBS_FILE, "w") as f:
        json.dump({"jobs": data}, f, indent=2)
