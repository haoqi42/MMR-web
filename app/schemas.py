from datetime import datetime

from pydantic import BaseModel

class gameResponse(BaseModel):
    id: int
    player1_id: int
    player1_name: str
    player2_id: int
    player2_name: str
    winner_id: int
    winner_name: str
    date: datetime

class gameCreateRequest(BaseModel):
    player1_name: str
    player2_name: str
    winner_name: str

class playerCreateRequest(BaseModel):
    name: str
    rank: str = "30 Kyu"

class playerResponse(BaseModel):
    name: str
    rank: str

class loginRequest(BaseModel):
    username: str
    password: str