import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import json
import re
from pathlib import Path

# --------------------------
# Setup
# --------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "chunks.json"
VECTOR_PATH = BASE_DIR / "vector_db"

# small + fast embedding model (good quality)
EMBEDDER = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client(
    Settings(
        persist_directory=str(VECTOR_PATH),
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection(
    name="project_chunks"
)

# --------------------------
# Load chunks
# --------------------------

def load_chunks():
    if not DATA_PATH.exists():
        print("❌ chunks.json not found")
        return []

    data = json.loads(DATA_PATH.read_text())
    print(f"✅ Loaded {len(data)} chunks")
    return data


def ensure_index_exists():
    if collection.count() == 0:
        print("⚙ No vectors found — building index...")
        ingest_chunks()
    else:
        print(f"✅ Vector index already exists: {collection.count()} chunks")


# --------------------------
# Embed + store
# --------------------------

def ingest_chunks():
    chunks = load_chunks()
    if not chunks:
        return
    
    existing = set(collection.get()["ids"])

    docs = []
    meta = []
    ids = []

    for d in chunks:
        vid = f"{d['hash']}:{d['chunk_id']}"

        if vid in existing:
            continue

        ids.append(f"{d['hash']}:{d['chunk_id']}")
        docs.append(d["text"])
        meta.append({
            "file": d["file"],
            "hash": d["hash"],
            "chunk": d["chunk_id"]
        })

    if not ids:
        print("✅ No new chunks to add.")
        return

    print("⚙ Generating embeddings...")
    vectors = EMBEDDER.encode(docs)

    print("📥 Storing embeddings in Chroma...")
    collection.add(
        documents=docs,
        embeddings=vectors,
        metadatas=meta,
        ids=ids
    )

    print(f"✅ Added {len(ids)} new vectors.")


# --------------------------
# Semantic search
# --------------------------

def query_db(query: str, k: int = 3):
    ensure_index_exists()

    query_vector = EMBEDDER.encode(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results.get("distances", [[None] * len(docs)])[0]

    response = []
    for doc, meta, dist in zip(docs, metas, distances):
        formatted = doc

        # Normalize slide boundary text → visual separator
        formatted = re.sub(
            r"(?i)\bslide\s+\d+\s+break\b",
            "\n\n──────── Slide Break ────────\n\n",
            formatted,
        )

        # Whitespace cleanup (preserve \n)
        formatted = re.sub(r"[ \t]+", " ", formatted)
        formatted = re.sub(r"\n\s*\n+", "\n\n", formatted)
        full = formatted.strip()

        # create a snippet (first 400 chars)
        snippet = full
        if len(snippet) > 400:
            snippet = snippet[:400] + "..."


        response.append(
            {
                "file": meta.get("file"),
                "chunk": meta.get("chunk"),
                "hash": meta.get("hash"),
                "snippet": snippet,
                "full": full,
                "distance": dist,
            }
        )
    
    # ensure best matches first
    response.sort(key=lambda x: x["distance"] if x["distance"] is not None else 999)
    deduped = []
    seen = set()

    for r in response:
        sig = r["snippet"][:120]
        if sig in seen:
            continue
        seen.add(sig)
        deduped.append(r)

    response = deduped


    return response


def list_indexed_files():
    """
    Return list of files that have vectors in the collection,
    with hash and number of chunks per file.
    """
    ensure_index_exists()

    res = collection.get(include=["metadatas"])
    metas = res.get("metadatas") or []

    files = {}

    for m in metas:
        if not isinstance(m, dict):
            # in case Chroma ever returns nested lists
            continue

        fname = m.get("file")
        fh = m.get("hash")

        if not fname:
            continue

        key = (fname, fh)
        files.setdefault(key, 0)
        files[key] += 1

    result = []
    for (fname, fh), cnt in files.items():
        result.append(
            {
                "file": fname,
                "hash": fh,
                "chunks": cnt,
            }
        )

    return result


def get_index_stats():
    """
    Basic stats for UI/debug: total chunks, total files.
    """
    ensure_index_exists()
    files = list_indexed_files()
    return {
        "total_chunks": collection.count(),
        "total_files": len(files),
        "files": files,
    }


# --------------------------
if __name__ == "__main__":
    ingest_chunks()

    while True:
        q = input("\nAsk something (or 'exit'): ")

        if q.lower() == "exit":
            break

        results = query_db(q, k=3)

        print("\n📄 Search Results:")
        for r in results:
            print("-------------------------------------------------")
            print("FILE:", r["file"])
            print("CHUNK:", r["chunk"])
            print("TEXT:", r["text"][:300])

