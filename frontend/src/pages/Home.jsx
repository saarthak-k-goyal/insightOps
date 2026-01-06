// src/pages/Home.jsx
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="page">
      <h1 className="page-title">InsightOps</h1>
      <p className="page-subtitle">
        Upload your notes, slides, and PDFs, then search them semantically.
      </p>
      <p className="page-body">
        The backend is already indexing your CN / SE / DS docs with embeddings and
        Chroma. Use the search page to query them using natural language.
      </p>
      <Link to="/search" className="primary-btn">
        Go to Search
      </Link>
    </div>
  );
}
