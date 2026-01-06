import re
import json
from pathlib import Path
from threading import Lock
from config import DATA_PATH

file_lock = Lock()

def clean_text(text):
    """
    Normalize raw text:
    - lowercase
    - remove extra spaces
    - remove junk symbols
    """
    text = text.lower()
    text = re.sub(r'[^\w\s.,!?]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def chunk_text(text, chunk_size=300):
    """
    Split text into chunks safe for embeddings.
    (300 words default)
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

def save_chunks(file_name, file_hash, chunks):
    DATA_PATH.parent.mkdir(exist_ok=True)

    data = []

    if DATA_PATH.exists():
        try:
            text = DATA_PATH.read_text().strip()
            if text:
                data = json.loads(text)
        except json.JSONDecodeError:
            print("⚠ Corrupted or empty chunks.json detected – resetting store")
            data = []

    for i, chunk in enumerate(chunks):
        data.append({
            "file": file_name,
            "hash": file_hash,
            "chunk_id": i,
            "text": chunk
        })

    with file_lock:
        DATA_PATH.write_text(json.dumps(data, indent=2))
