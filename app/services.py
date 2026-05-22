from models import Player, Game
from rating import update, elo_to_rank, rank_to_elo
from fastapi import HTTPException
from datetime import datetime

#create player in database, returns player object
def create_player_in_db(db, name: str, rank: str):
    try:
        rating = rank_to_elo(rank)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid rank")

    if rating < 0:
        raise HTTPException(status_code=400, detail="Invalid rank")

    if (db.query(Player).filter(Player.name == name).first()):
        raise HTTPException(status_code=400, detail="Player with this name already exists")
    
    player = Player(name=name, rating=rating)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player

#get all players from database, returns list of player objects
def get_players_from_db(db):
    players = db.query(Player).all()

    return [
        {
            "name": player.name,
            "rank": elo_to_rank(player.rating)
        } for player in players
    ]

#get player by name, returns player object
def get_player_by_name(db, name: str):
    player = db.query(Player).filter(Player.name == name).first()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    return {
        "name": player.name,
        "rank": elo_to_rank(player.rating)
    }

#record match in database, returns game object
def record_match_by_name(db, p1_name: str, p2_name: str, winner_name: str):

    if (winner_name != p1_name) and (winner_name != p2_name):
        raise HTTPException(status_code=400, detail="Winner must be one of the players")
    
    p1 = db.query(Player).filter(Player.name == p1_name).first()
    p2 = db.query(Player).filter(Player.name == p2_name).first()
    winner = db.query(Player).filter(Player.name == winner_name).first()

    if not p1:
        raise HTTPException(status_code=404, detail=f"Player {p1_name} not found")
    if not p2:
        raise HTTPException(status_code=404, detail=f"Player {p2_name} not found")
    if not winner:
        raise HTTPException(status_code=404, detail=f"Player {winner_name} not found")

    return record_match_in_db(db, p1.id, p2.id, winner.id)

#record match in database, returns game object
def record_match_in_db(db, p1_id: int, p2_id: int, winner_id: int):

    #retrieve players and update ratings
    if winner_id not in [p1_id, p2_id]:
        raise HTTPException(status_code=400, detail="Winner must be one of the players")
    if p1_id == p2_id:
        raise HTTPException(status_code=400, detail="Players must be different")

    p1 = db.get(Player, p1_id)
    p2 = db.get(Player, p2_id)
    if not p1:
        raise HTTPException(status_code=404, detail=f"Player {p1_id} not found")
    if not p2:
        raise HTTPException(status_code=404, detail=f"Player {p2_id} not found")
    #add game record

    s1 = 1 if winner_id == p1_id else 0
    s2 = 1 - s1
    p1.ratingBefore = p1.rating
    p2.ratingBefore = p2.rating
    p1.rating, p2.rating = update(p1.rating, p2.rating, s1)

    #update games played and k factor
    p1.games_played += 1
    p2.games_played += 1
    if p1.games_played > 10:
        p1.k_factor = 50
    if p2.games_played > 10:
        p2.k_factor = 50
    db.commit()

    game = Game(
        player1_id=p1_id, 
        player2_id=p2_id, 
        winner_id=winner_id, 
        player1_rating_before=p1.ratingBefore, 
        player1_rating_after=p1.rating, 
        player2_rating_before=p2.ratingBefore, 
        player2_rating_after=p2.rating,
        date=datetime.now().date().isoformat()
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    
    return {
        "id": game.id,
        "player1_id": game.player1_id,
        "player1_name": p1.name,
        "player1_rating_before": game.player1_rating_before,
        "player1_rating_after": game.player1_rating_after,
        "player2_id": game.player2_id,
        "player2_name": p2.name,
        "player2_rating_before": game.player2_rating_before,
        "player2_rating_after": game.player2_rating_after,
        "winner_id": game.winner_id,
        "winner_name": p1.name if winner_id == p1_id else p2.name,
        "date": game.date,
    }

#get all games from database, returns list of game objects
def get_games_from_db(db):
    games = db.query(Game).all()

    games.sort(key=lambda g: g.date, reverse=True)

    #returning as dict in the form of pydantic object
    return [
        {
            "id": game.id,
            "player1_id": game.player1_id,
            "player1_name": game.player1.name,
            "player2_id": game.player2_id,
            "player2_name": game.player2.name,
            "winner_id": game.winner_id,
            "winner_name": game.winner.name,
            "date": game.date
        }
        for game in games
    ]

