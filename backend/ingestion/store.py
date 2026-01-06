import json
import os
from config import METADATA_PATH

def load_db():
    if not os.path.exists(METADATA_PATH):
        return []
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_db(data):
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def add_metadata(entry) -> bool:
    """
    Adds metadata entry only if hash is not already present.
    Returns True if added, False if skipped.
    """
    db = load_db()

    new_hash = entry.get("hash")
    if not new_hash:
        raise ValueError("Metadata entry missing 'hash'")

    # 🔒 Idempotency check
    for item in db:
        if item.get("hash") == new_hash:
            return False  # already indexed

    db.append(entry)
    save_db(db)
    return True
