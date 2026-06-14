import { useState, useEffect } from "react";
import { Routes, Route, Link } from "react-router-dom";
import PlayersPage from "./PlayersPage";
import GamesPage from "./GamesPage";
import RecordGamePage from "./RecordGamePage";
import AddPlayerPage from "./AddPlayerPage";
import LoginPage from "./LoginPage";

function App() {
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;

    fetch("http://localhost:8000/me", {
      headers: { "Authorization": `Bearer ${token}` }
    })
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data?.role === "admin") setIsAdmin(true);
      });
  }, []);

  return (
    <div>
      <nav>
        <Link to="/">Players</Link>
        <Link to="/games">Games</Link>
        {isAdmin && <Link to="/record-game">Record Game</Link>}
        {isAdmin && <Link to="/add-player">Add Player</Link>}
        <Link to="/login" className="nav-login-btn">
          {isAdmin ? "Account" : "Login"}
        </Link>
      </nav>

      <Routes>
        <Route path="/" element={<PlayersPage />} />
        <Route path="/games" element={<GamesPage />} />
        <Route path="/record-game" element={<RecordGamePage />} />
        <Route path="/add-player" element={<AddPlayerPage />} />
        <Route path="/login" element={<LoginPage setIsAdmin={setIsAdmin} />} />
      </Routes>
    </div>
  );
}

export default App;
