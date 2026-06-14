import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function LoginPage({ setIsAdmin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loggedInAs, setLoggedInAs] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setLoading(false);
      return;
    }

    fetch("http://localhost:8000/me", {
      headers: { "Authorization": `Bearer ${token}` }
    })
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data) setLoggedInAs(data.username);
        setLoading(false);
      });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      setMessage("Invalid username or password.");
      return;
    }

    const data = await response.json();
    localStorage.setItem("token", data.access_token);
    setLoggedInAs(username);
    setIsAdmin(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setLoggedInAs(null);
    setIsAdmin(false);
  };

  if (loading) return null;

  if (loggedInAs) {
    return (
      <div className="page">
        <h1>Admin Login</h1>
        <div className="card">
          <p style={{ color: "var(--text)", marginBottom: "16px" }}>
            Logged in as <strong>{loggedInAs}</strong>
          </p>
          <button type="button" onClick={handleLogout} style={{ background: "var(--red)" }}>
            Logout
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <h1>Admin Login</h1>
      <div className="card">
        <form onSubmit={handleSubmit}>
          <label>
            Username
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </label>

          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>

          <button type="submit">Login</button>
        </form>

        {message && <p className="message error">{message}</p>}
      </div>
    </div>
  );
}
