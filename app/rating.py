import math

K = 100

#Returns the expected score of player 1 against player 2, score is 1 if player 1 wins, 0 if player 2 wins
def expected(r1, r2):
    return 1 / (1 + 10 ** ((r2 - r1) / 400))

#returns a pair of integers, the new ratings for player 1 and player 2 after a match. Score is 1 if player 1 wins, 0 if player 2 wins
def update(r1, r2, score, handicap=0):
    r1 += handicap
    e = expected(r1, r2)
    return r1 + K * (score - e), r2 + K * ((1 - score) - (1 - e))

#Converts an Elo rating to a Go rank, where 30 Kyu is the lowest rank and 9 Dan is the highest. Ranks are in increments of 100 Elo points, with 30 Kyu at 0 Elo
def elo_to_rank(rating):
    if rating < 2900:
        return str(int(30 - rating//100)) + " Kyu"
    else:
        return str(int(rating//100 - 28)) + " Dan"

#converts go rank to elo rating
def rank_to_elo(rank):
    if "Kyu" in rank:
        return (30 - int(rank.split()[0])) * 100
    else:
        return (int(rank.split()[0]) + 28) * 100