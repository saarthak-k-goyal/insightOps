from pathlib import Path

# backend/
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "ingest_queue"
PROCESSED_DIR = BASE_DIR / "processed"
VECTOR_PATH = BASE_DIR / "vector_db"

DATA_PATH = DATA_DIR / "chunks.json"
METADATA_PATH = DATA_DIR / "metadata.json"
