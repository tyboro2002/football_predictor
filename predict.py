from game import FootballGame
import random


def predict(game: FootballGame):
    return random.choice([game.team1, game.team2, "draw"])
