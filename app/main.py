from fastapi import FastAPI, Depends
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import Player, Game
from rating import update
import services
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",  # Vite frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/players")
def get_players(db: Session = Depends(get_db), response_model=list[schemas.playerResponse]):
    return services.get_players_from_db(db)

@app.get("/players/{name}")
def get_player(name: str, db: Session = Depends(get_db), response_model=schemas.playerResponse):
    return services.get_player_by_name(db, name)

@app.post("/player")
def create_player(player: schemas.playerCreateRequest, db: Session = Depends(get_db)):
    return services.create_player_in_db(
        db, 
        player.name, 
        player.rank
    )

@app.post("/match/{p1_id}/{p2_id}/{winner_id}")
def record_match(p1_id: int, p2_id: int, winner_id: int, db: Session = Depends(get_db)):
    #add game record
    return services.record_match_in_db(db, p1_id, p2_id, winner_id)

@app.get("/games", response_model=list[schemas.gameResponse])
def get_games(db: Session = Depends(get_db)):
    return services.get_games_from_db(db)

@app.post("/game")
def record_match_by_name(game: schemas.gameCreateRequest, db: Session = Depends(get_db)):
    return services.record_match_by_name(
        db,
        game.player1_name,
        game.player2_name,
        game.winner_name
    )