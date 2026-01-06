// src/components/SearchBar.jsx
export default function SearchBar({ query, setQuery, onSubmit, loading }) {
  return (
    <form className="search-bar" onSubmit={onSubmit}>
      <input
        className="search-input"
        type="text"
        placeholder="Search your notes... (e.g. 'TCP 3-way handshake')"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button className="primary-btn" type="submit" disabled={loading}>
        {loading ? "Searching..." : "Search"}
      </button>
    </form>
  );
}
