// src/App.jsx
import { Link, Routes, Route, useLocation } from "react-router-dom";
import Home from "./pages/Home";
import Search from "./pages/Search";

export default function App() {
  const location = useLocation();

  return (
    <div className="app-root">
      <header className="app-header">
        <div className="app-logo">InsightOps</div>
        <nav className="app-nav">
          <Link
            to="/"
            className={location.pathname === "/" ? "nav-link active" : "nav-link"}
          >
            Home
          </Link>
          <Link
            to="/search"
            className={
              location.pathname === "/search" ? "nav-link active" : "nav-link"
            }
          >
            Search
          </Link>
        </nav>
      </header>

      <main className="app-main">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<Search />} />
        </Routes>
      </main>
    </div>
  );
}
