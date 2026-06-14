import { useEffect, useState } from "react";

function PlayersPage() {
  const [players, setPlayers] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/players")
      .then((res) => res.json())
      .then((data) => setPlayers(data));
  }, []);

  return (
    <div className="page">
      <h1>Players</h1>
      <div className="card">
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "14px" }}>
          <thead>
            <tr>
              <th style={{ textAlign: "left", padding: "10px 14px", color: "var(--text-muted)", fontSize: "12px", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.5px", borderBottom: "1px solid var(--border)" }}>Name</th>
              <th style={{ textAlign: "left", padding: "10px 14px", color: "var(--text-muted)", fontSize: "12px", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.5px", borderBottom: "1px solid var(--border)" }}>Rank</th>
            </tr>
          </thead>
          <tbody>
            {players.map((p, i) => (
              <tr key={i} style={{ borderBottom: "1px solid var(--border)" }}>
                <td style={{ padding: "12px 14px", color: "var(--text)" }}>{p.name}</td>
                <td style={{ padding: "12px 14px", color: "var(--green)", fontWeight: 600 }}>{p.rank}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default PlayersPage;