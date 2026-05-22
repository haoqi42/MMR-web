import { useEffect, useState } from "react";

function PlayersPage() {
  const [players, setPlayers] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/players")
      .then((res) => res.json())
      .then((data) => setPlayers(data));
  }, []);

  return (
    <div>
      <h1>Elo Ratings</h1>

      <ul>
        {players.map((p) => (
          <li key={p.id}>
            {p.name} - {p.rank}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PlayersPage;