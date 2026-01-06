from fastapi import FastAPI, Query, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from vector_store.store import query_db, list_indexed_files, get_index_stats

from pathlib import Path
from ingestion.ingest import process_file

from config import UPLOAD_DIR

UPLOAD_DIR.mkdir(exist_ok=True)


app = FastAPI(title="InsightOps Search API")

# CORS for React (we'll use this from the frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to http://localhost:5173 or your deployed frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search")
def search(q: str = Query(..., min_length=1), k: int = 5):
    results = query_db(q, k)
    return {
        "query": q,
        "count": len(results),
        "results": results,
    }


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing")

    # only allow types we can handle
    allowed_ext = (".pdf", ".pptx", ".txt")
    lower = file.filename.lower()
    if not lower.endswith(allowed_ext):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_ext)}",
        )

    dest_path = UPLOAD_DIR / file.filename

    try:
        contents = await file.read()
        dest_path.write_bytes(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # run the same processing pipeline as the watcher
    try:
        result = process_file(str(dest_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to index file: {e}")

    if result.get("status") == "skipped":
        return {
            "status": "ok",
            "file": result["filename"],
            "hash": result["hash"],
            "message": "File already indexed.",
        }

    return {
        "status": "ok",
        "file": file.filename,
        "chunks": result.get("chunks") if result else None,
        "message": "File uploaded and indexed successfully.",
    }



@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/files")
def files():
    files = list_indexed_files()
    return {
        "count": len(files),
        "files": files,
    }


@app.get("/stats")
def stats():
    return get_index_stats()
