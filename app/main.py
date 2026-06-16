from fastapi import FastAPI, Depends
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from auth import get_current_user, require_admin
from database import engine, Base, SessionLocal, get_db
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



@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/players")
def get_players(db: Session = Depends(get_db), response_model=list[schemas.playerResponse]):
    return services.get_players_from_db(db)

@app.get("/players/{name}")
def get_player(name: str, db: Session = Depends(get_db), response_model=schemas.playerResponse):
    return services.get_player_by_name(db, name)

@app.get("/games", response_model=list[schemas.gameResponse])
def get_games(db: Session = Depends(get_db)):
    return services.get_games_from_db(db)

@app.get("/players/{name}/games", response_model=list[schemas.gameResponse])
def get_player_games(name: str, db: Session = Depends(get_db)):
    return services.get_games_for_player(db, name)

@app.get("/players/{name}/graph", response_model=list)
def get_player_rank_history(name: str, db: Session = Depends(get_db)):
    return services.get_rank_history(db, name)

#------------------------------------------------------------------------------------------------------------
# These requests are gated by rbac (Admins only can access)
#------------------------------------------------------------------------------------------------------------

@app.post("/player")
def create_player(player: schemas.playerCreateRequest, db: Session = Depends(get_db), _=Depends(require_admin)):
    return services.create_player_in_db(
        db, 
        player.name, 
        player.rank
    )


@app.post("/game")
def record_match_by_name(game: schemas.gameCreateRequest, db: Session = Depends(get_db), _=Depends(require_admin)):
    return services.record_match_by_name(
        db,
        game.player1_name,
        game.player2_name,
        game.winner_name
    )


#------------------------------------------------------------------------------------------------------------
# Login/logout
#------------------------------------------------------------------------------------------------------------

@app.post("/login")
def login(credentials: schemas.loginRequest, db: Session = Depends(get_db)):
    return services.login(db, credentials.username, credentials.password)

@app.get("/me")
def me(current_user=Depends(get_current_user)):
      return {"username": current_user.username, "role": current_user.role}