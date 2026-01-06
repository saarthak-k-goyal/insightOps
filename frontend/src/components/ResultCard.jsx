import { useState } from "react";

export default function ResultCard({ result }) {
  const { file, chunk, snippet, full, distance } = result;
  const [expanded, setExpanded] = useState(false);

  const score =
    typeof distance === "number" ? (1 / (1 + distance)).toFixed(2) : null;

  const canExpand = full && full.length > snippet.length;

  return (
    <article className="result-card">
      <header className="result-header">
        <div className="result-file">{file}</div>
        <div className="result-meta">
          <span>Chunk #{chunk}</span>
          {score && <span className="result-score">Score: {score}</span>}
        </div>
      </header>

      <pre className="result-snippet">
        {expanded && canExpand ? full : snippet}
      </pre>

      {canExpand && (
        <button
          type="button"
          className="link-btn"
          onClick={() => setExpanded((v) => !v)}
        >
          {expanded ? "Collapse" : "Expand"}
        </button>
      )}
    </article>
  );
}
