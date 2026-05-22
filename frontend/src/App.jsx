import { Routes, Route, Link } from "react-router-dom";
import PlayersPage from "./PlayersPage";
import GamesPage from "./GamesPage";
import RecordGamePage from "./RecordGamePage";
import AddPlayerPage from "./AddPlayerPage";

function App() {
  return (
    <div>
      <nav>
        <Link to="/">Players</Link> |{" "}
        <Link to="/games">Games</Link> |{" "}
        <Link to="/record-game">Record Game</Link> |{" "}
        <Link to="/add-player">Add Player</Link>
      </nav>

      <Routes>
        <Route path="/" element={<PlayersPage />} />
        <Route path="/games" element={<GamesPage />} />
        <Route path="/record-game" element={<RecordGamePage />} />
        <Route path="/add-player" element={<AddPlayerPage />} />
      </Routes>
    </div>
  );
}

export default App;