from game import FootballGame
from formats import League
import random


def predict_game(game: FootballGame, silent: bool = True):
    home_goals = random.randint(0, 5)
    away_goals = random.randint(0, 5)
    game.home_score = home_goals
    game.away_score = away_goals
    if not silent:
        print(f"{game.home} {game.home_score} - {game.away} {game.away_score}")
    return game
    # return random.choice([game.home, game.away, "draw"])


def predict_league(inp_league: League, silent: bool = True):
    league = inp_league.copy()
    playday = 1
    for matchday in league.matchdays:
        if not silent:
            print("day", playday)
        playday += 1
        for match in matchday:
            prediction = predict_game(match, silent)
            if not silent:
                print(match.home, "VS", match.away, "results in", prediction)
            league.record_match_result(match.home, match.away, prediction.home_score, prediction.away_score)
    if not silent:
        print(league)
    return league
