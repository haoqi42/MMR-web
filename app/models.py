from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    rating = Column(Float, default=800)
    k_factor = Column(Float, default=200)
    games_played = Column(Integer, default=0)
    date = Column(DateTime, server_default=func.now())

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    player1_id = Column(Integer, ForeignKey("players.id"), index=True)
    player1_rating_before = Column(Float)
    player1_rating_after = Column(Float)
    player2_id = Column(Integer, ForeignKey("players.id"), index=True)
    player2_rating_before = Column(Float)
    player2_rating_after = Column(Float)
    winner_id = Column(Integer, ForeignKey("players.id"), index=True)
    date = Column(DateTime, server_default=func.now())
    result = Column(String)

    player1 = relationship("Player", foreign_keys=[player1_id])
    player2 = relationship("Player", foreign_keys=[player2_id])
    winner = relationship("Player", foreign_keys=[winner_id])

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="admin", nullable=False)