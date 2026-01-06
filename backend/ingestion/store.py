import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # backend/
DB_PATH = BASE_DIR / "data" / "metadata.json"

def load_db():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def save_db(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def add_metadata(entry):
    db = load_db()
    db.append(entry)
    save_db(db)
