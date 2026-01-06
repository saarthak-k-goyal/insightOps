# InsightOps

InsightOps is a local-first semantic search system for personal documents (PDFs, PPTX, TXT).  
It ingests files, extracts and chunks text, generates embeddings, and allows semantic search via a clean React UI.

The system is **idempotent**, meaning the same document is never indexed twice, even if uploaded again.

---

## Features

- Semantic search over notes, PDFs, and slides
- Idempotent document ingestion using content hashing (SHA-256)
- Slide-aware chunking for PPTX files
- Duplicate detection and safe re-uploads
- REST API built with FastAPI
- Clean React frontend (Vite)
- Local-first (no paid services, no cloud dependency)

---

## Tech Stack

### Backend
- Python 3
- FastAPI
- sentence-transformers
- ChromaDB (vector store)

### Frontend
- React
- Vite
- Fetch API

---

## Architecture Overview

- File Upload → Ingestion Layer (hashing, duplicate detection, extraction) → Processing Layer (cleaning, chunking) → Vector Store (embeddings in ChromaDB) → Search API → React Frontend

---

## Project Structure
```
insightOps/
├── backend/
│ ├── api/ # FastAPI routes
│ ├── ingestion/ # File ingestion & hashing
│ ├── processing/ # Text cleaning & chunking
│ ├── vector_store/ # Embedding + ChromaDB logic
│ ├── data/ # Runtime data (ignored in git)
│ └── config.py
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ ├── pages/
│ │ └── App.jsx
│ └── vite.config.js
└── README.md
```
---

## How Idempotent Ingestion Works

1. A SHA-256 hash is computed from file contents
2. Metadata is checked for existing hash
3. If hash exists → ingestion is skipped
4. If hash is new → file is processed and indexed

This prevents:
- Duplicate chunks
- Duplicate embeddings
- Metadata corruption

---

## How to Run Locally

### Backend

```
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn api.routes:app --reload
```
Backend runs at: http://127.0.0.1:8000

---

### Frontend

```
cd frontend
npm install
npm run dev
```
Frontend runs at: http://localhost:5173

---

## Example Queries

- Explain HTTP methods
- What is abstraction in software design
- Steps of DNS resolution
- Difference between URI and URL

---

## What I Learned

- Designing idempotent ingestion pipelines
- Practical use of embeddings and vector search
- Handling real document formats (PDF, PPTX)
- Backend–frontend integration with clear contracts
- Avoiding duplicate state in distributed workflows

This project strengthened my understanding of backend system design,
idempotent pipelines, and practical semantic search.

---

## Future Improvements

- Highlight matched sentences inside chunks
- Chunk expansion / collapse in UI
- Better slide segmentation for PPTX
- Optional summaries using LLMs

---

## License
MIT

---