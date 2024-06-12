from models.game import FootballGame
from models.formats import League, GroupStage, KnockoutStage
import random


def predict_game(game: FootballGame, silent: bool = True):
    if not game.home.position_prev_season == 0 and not game.away.position_prev_season == 0:
        # Adjust goal probability based on the previous season's position
        home_position_factor = max(1,
                                   20 - game.home.position_prev_season)  # Lower position number should mean better team
        away_position_factor = max(1,
                                   20 - game.away.position_prev_season)  # Lower position number should mean better team

        home_goals = max(0,
                         random.gauss(home_position_factor / 5,
                                      1.0))  # Gaussian distribution centered on position factor
        away_goals = max(0,
                         random.gauss(away_position_factor / 5,
                                      1.0))  # Gaussian distribution centered on position factor

        # Converting goal predictions to integers
        game.home_score = int(home_goals)
        game.away_score = int(away_goals)

        if not silent:
            print(f"{game.home.name} {game.home_score} - {game.away.name} {game.away_score}")

        return game
    else:
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
            if match.home_score is None or match.away_score is None:
                prediction = predict_game(match, silent)
                league.record_match_result(match.home, match.away, prediction.home_score, prediction.away_score)
            else:
                prediction = match
            if not silent:
                print(match.home, "VS", match.away, "results in", prediction)
    if not silent:
        print(league)
    return league


def predict_group_stage(groups: GroupStage, silent: bool = True):
    groups.leagues = [predict_league(league, silent) for league in groups.leagues]
    return groups


def predict_knockout(knock_out: KnockoutStage, silent: bool = True):
    while len(knock_out.current_round) > 1:
        # Record results for the round
        for game in knock_out.current_round:
            game = predict_game(game, silent)
            knock_out.record_match_result(game)

        # Progress to the next round
        knock_out.progress_to_next_round()

    # Record results for the last round
    for game in knock_out.current_round:
        game = predict_game(game, silent)
        knock_out.record_match_result(game)

    return knock_out
