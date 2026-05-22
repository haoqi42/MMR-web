import { useEffect, useState } from "react";
import "./styles/GamesPage.css";

function GamesPage() {
  const [games, setGames] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/games")
      .then((res) => res.json())
      .then((data) => setGames(data))
      .catch((err) => console.error("Failed to fetch games:", err));
  }, []);

  return (
    <div className="games-page">
      <h1>Games</h1>

      <table className="games-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Black</th>
            <th>White</th>
            <th>Winner</th>
            <th>Date</th>
          </tr>
        </thead>

        <tbody>
          {games.map((game) => (
            <tr key={game.id}>
              <td>{game.id}</td>
              <td>{game.player1_name}</td>
              <td>{game.player2_name}</td>
              <td>{game.winner_name}</td>
              <td>{game.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default GamesPage;