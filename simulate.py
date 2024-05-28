from predict import predict_game, predict_league
from game import FootballGame
from formats import League


def simulate_game(game: FootballGame, n):
    outcomes = {"home_win": 0, "draw": 0, "away_win": 0}

    for _ in range(n):
        result = predict_game(game)
        if result.home_score > result.away_score:
            outcomes["home_win"] += 1
        if result.home_score == result.away_score:
            outcomes["draw"] += 1
        if result.home_score < result.away_score:
            outcomes["away_win"] += 1

    home_win_chance = outcomes["home_win"] / n
    draw_chance = outcomes["draw"] / n
    away_win_chance = outcomes["away_win"] / n

    return {"home_win": home_win_chance, "draw": draw_chance, "away_win": away_win_chance}

def simulate_league(league: League, n):
    position_counts = {team: [0 for _ in range(len(league.teams))] for team in league.teams}

    for _ in range(n):
        standings = predict_league(league).get_standings()
        for i in range(len(standings)):
            team = standings[i][0]
            position_counts[team][i] += 1

    for e in position_counts.keys():
        old = position_counts[e]
        new = []
        for ell in old:
            new.append(ell / n)
        position_counts[e] = new

    return position_counts
