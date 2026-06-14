import { useEffect, useState } from "react";

export default function RecordGamePage() {
  const [p1_name, setP1_name] = useState("");
  const [p2_name, setP2_name] = useState("");
  const [winner_name, setWinner_name] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    if (!token) {
      setMessage("You must be logged in as an admin to record a game.");
      return;
    }
    const response = await fetch(`http://localhost:8000/game`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify({
        player1_name: p1_name,
        player2_name: p2_name,
        winner_name: winner_name
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      if (response.status === 404 || response.status === 400) {
        setMessage(error.detail);
      }
      return;
    }

    setMessage("Game recorded successfully!");
    setP1_name("");
    setP2_name("");
    setWinner_name("");
  };

  return (
    <div className="page">
      <h1>Record Game</h1>
      <div className="card">
        <form onSubmit={handleSubmit}>
          <label>
            Player 1
            <input
              type="text"
              value={p1_name}
              onChange={(e) => setP1_name(e.target.value)}
              placeholder="Enter player name"
              required
            />
          </label>

          <label>
            Player 2
            <input
              type="text"
              value={p2_name}
              onChange={(e) => setP2_name(e.target.value)}
              placeholder="Enter player name"
              required
            />
          </label>

          <label>
            Winner
            <input
              type="text"
              value={winner_name}
              onChange={(e) => setWinner_name(e.target.value)}
              placeholder="Enter player name"
              required
            />
          </label>

          <button type="submit">Record Game</button>
        </form>

        {message && <p className="message">{message}</p>}
      </div>
    </div>
  );
}