# Elo App

A simple Elo rating application with a backend API and frontend client.

---

## Prerequisites

Make sure you have the following installed:

* Python 3.12+
* Node.js (v18+ recommended)
* npm
* SQLite (usually included with Python)

---

## Project Structure

```
.
├── app/        # FastAPI backend
├── frontend/       # Frontend (Vite / React)
├── db.sqlite3      # SQLite database (auto-created)
└── README.md
```

---

## Backend Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Navigate to the backend directory:

```bash
cd app
```

Run the backend server:

```bash
  uvicorn main:app --reload
```

Backend will be available at:

```
http://localhost:8000
```

API documentation:

```
http://localhost:8000/docs
```

---

## Database

This application uses SQLite.

* Database file: `db.sqlite3`
* Automatically created on first run
* No separate service required (SQLite runs in-process)

## Resetting the Database

The backend uses a local SQLite database file named `db.sqlite3`.

If you want to completely reset the database (remove all players, games, ratings, etc.), follow these steps.

### 1. Stop the Backend Server

If the FastAPI server is running, stop it first.

Example:
```bash
CTRL + C
```
In the directory with the database, run the following:

```
rm db.sqlite3
```

---

## Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend will be available at:

```
http://localhost:5173
```

---

## Running the Full Application

Start backend:

```bash
cd app
uvicorn main:app --reload
```

Start frontend (in another terminal):

```bash
cd frontend
npm run dev
```

Then open:

```
http://localhost:5173
```

---

## Example API Usage

Create a player:

```bash
curl -X POST http://localhost:8000/players \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "rating": 1200}'
```

Get all players:

```bash
curl http://localhost:8000/players
```

Get a specific player:

```bash
curl http://localhost:8000/players/1
```

---

## Notes

* If you get a `UNIQUE constraint failed: players.name` error, it means a player with that name already exists.
* Delete `db.sqlite3` to reset the database during development.
* Make sure backend is running before starting the frontend.

---
