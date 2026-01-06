This follows an intellectual architecture broken into 5 sub-layers

1) Data Ingestion Layer:
    point where files enter the system
    handles: txt, pdf, md files, notes, chats, snippets
    working: file watcher listens to folder -> modification of any sort triggers ingestion -> file goes to processing queue

2) Preprocessing Layer:
    takes raw data and clean it
    includes: text extraction, basic cleaning, metadata capture (metadat for semantic search)

3) Embeddings + Vector store layer:
    The "AI Brain"
    every text is converted into a vector
    Example:
        Search “how to scale databases” → returns document that talks about “load balancing sharding horizontal partitioning.”

4) Insight Engine:
    tasks: semantic search, summarries, trends, clustering similaar files
    uses: embeddings, LLMs, Statistical patterns, metadata

5) Presentation Layer (Frontend):
    Dashboard elements:
        Search bar (semantic search)
        Timeline heatmap (file activity over time)
        File clusters (groups of similar documents)
        Auto-generated insights
        Quick summaries
        “What changed today?”

    Tools:
        React + Tailwind
        Recharts (visualizations)

