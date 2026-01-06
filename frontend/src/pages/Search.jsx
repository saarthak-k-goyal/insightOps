// src/pages/Search.jsx
import { useState } from "react";
import { API_BASE_URL } from "../config";
import SearchBar from "../components/SearchBar";
import ResultCard from "../components/ResultCard";

export default function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");
  const [uploadError, setUploadError] = useState("");

  async function handleSearch(e) {
    e?.preventDefault();
    const trimmed = query.trim();
    if (!trimmed) return;

    setLoading(true);
    setError("");
    try {
      const url = `${API_BASE_URL}/search?q=${encodeURIComponent(trimmed)}&k=5`;
      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }
      const data = await res.json();
      setResults(data.results || []);
      setCount(data.count || 0);
    } catch (err) {
      console.error(err);
      setError("Could not fetch results. Check if backend is running.");
      setResults([]);
      setCount(0);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <h1 className="page-title">Semantic Search</h1>
      <p className="page-subtitle">
        Ask questions over your indexed notes (e.g. &quot;Explain HTTP&quot;,
        &quot;DNS resolution steps&quot;, &quot;Types of software testing&quot;).
      </p>

      <SearchBar
        query={query}
        setQuery={setQuery}
        onSubmit={handleSearch}
        loading={loading}
      />

      <div className="upload-section">
        <label className="upload-label">Upload document (PDF / PPTX / TXT):</label>
        <div className="upload-row">
          <input
            type="file"
            onChange={handleFileChange}
            className="upload-input"
            accept=".pdf,.pptx,.txt"
          />
          <button
            className="secondary-btn"
            onClick={handleUpload}
            disabled={uploading || !selectedFile}
            type="button"
          >
            {uploading ? "Uploading..." : "Upload & Index"}
          </button>
        </div>
        {uploadMessage && (
          <div className="alert alert-ok">{uploadMessage}</div>
        )}
        {uploadError && <div className="alert alert-error">{uploadError}</div>}
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {!loading && count > 0 && (
        <div className="results-summary">
          {count} result{count !== 1 ? "s" : ""} found
        </div>
      )}

      {loading && <div className="loading">Searching…</div>}

      <div className="results-list">
        {results.map((r, idx) => (
          <ResultCard key={`${r.hash}-${r.chunk}-${idx}`} result={r} />
        ))}
      </div>
    </div>
  );
  
  function handleFileChange(e) {
    const file = e.target.files?.[0] || null
    setSelectedFile(file);
    setUploadMessage("");
    setUploadError("");
  }
  
  async function handleUpload(e) {
    e?.preventDefault();
    if (!selectedFile) return;
  
    setUploading(true);
    setUploadMessage("");
    setUploadError("");
  
    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
  
      const res = await fetch(`${API_BASE_URL}/upload`, {
        method: "POST",
        body: formData,
      });
  
      if (!res.ok) {
        const data = await res.json().catch(() => null);
        const msg = data?.detail || `Upload failed (${res.status})`;
        throw new Error(msg);
      }
  
      const data = await res.json();
      setUploadMessage(data.message || "File uploaded and indexed.");
    } catch (err) {
      console.error(err);
      setUploadError(err.message || "Upload failed.");
    } finally {
      setUploading(false);
    }
  }
}

