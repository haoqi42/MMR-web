import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
import "./styles/GamesPage.css";

function PlayerPage() {
  const { name } = useParams();
  const [player, setPlayer] = useState(null);
  const [games, setGames] = useState([]);
  const [rankHistory, setRankHistory] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:8000/players/${name}`)
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => setPlayer(data));

    fetch(`http://localhost:8000/players/${name}/games`)
      .then((res) => (res.ok ? res.json() : []))
      .then((data) => setGames(data))
      .catch((err) => console.error("Failed to fetch player games:", err));

    fetch(`http://localhost:8000/players/${name}/graph`)
      .then((res) => (res.ok ? res.json() : []))
      .then((data) =>
        setRankHistory(
          data.map((point, index) => ({
            ...point,
            index,
          }))
        )
      )
      .catch((err) => console.error("Failed to fetch rank history:", err));
  }, [name]);

  return (
    <div className="games-page">
      <Link to="/">&larr; Back to Players</Link>
      <h1>{name}</h1>
      {player && <p>Rank: {player.rank}</p>}

      {rankHistory.length > 1 && (
        <div className="card" style={{ padding: "16px", marginBottom: "16px" }}>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={rankHistory}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="index"
                type="number"
                allowDecimals={false}
                domain={[0, rankHistory.length - 1]}
                tickFormatter={(idx) =>
                  rankHistory[idx]
                    ? new Date(rankHistory[idx].date).toLocaleDateString()
                    : ""
                }
              />
              <YAxis reversed domain={["auto", "auto"]} />
              <Tooltip
                labelFormatter={(idx) =>
                  rankHistory[idx]
                    ? new Date(rankHistory[idx].date).toLocaleDateString()
                    : ""
                }
                formatter={(value, _name, props) => [
                  `${value.toFixed(1)} ${props.payload.type}`,
                  "Rank",
                ]}
              />
              <Line type="monotone" dataKey="rank" stroke="var(--green)" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      <div className="card" style={{ padding: 0, overflow: "hidden" }}>
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
                <td>{new Date(game.date).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default PlayerPage;
