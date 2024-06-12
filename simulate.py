from predict import predict_game, predict_league, predict_knockout
from models.game import FootballGame
from models.formats import League, GroupStage, KnockoutStage
import multiprocessing
from math import log2, ceil


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


def simulate_once(league):
    standings = predict_league(league).get_standings()
    return [team for team, _ in standings]


def worker_simulation(league, n):
    num_teams = len(league.teams)
    position_counts = {team: [0] * num_teams for team in league.teams}

    for _ in range(n):
        standings = simulate_once(league)
        for i, team in enumerate(standings):
            position_counts[team][i] += 1

    return position_counts


def combine_results(results, num_teams):
    combined_counts = {team: [0] * num_teams for team in results[0]}

    for result in results:
        for team, counts in result.items():
            for i, count in enumerate(counts):
                combined_counts[team][i] += count

    return combined_counts


def simulate_league(league: League, n: int, num_workers: int = None):
    num_teams = len(league.teams)

    if num_workers is None:
        num_workers = multiprocessing.cpu_count()

    simulations_per_worker = n // num_workers
    remaining_simulations = n % num_workers
    tasks = [simulations_per_worker + (1 if i < remaining_simulations else 0) for i in range(num_workers)]

    with multiprocessing.Pool(num_workers) as pool:
        results = pool.starmap(worker_simulation, [(league, task) for task in tasks])

    combined_counts = combine_results(results, num_teams)

    for team in combined_counts:
        combined_counts[team] = [count / n for count in combined_counts[team]]

    return combined_counts


def simulate_group_stage(groups: GroupStage, n: int, num_workers: int = None):
    outp_positions = []
    for league in groups.leagues:
        simulated_positions = simulate_league(league, n, num_workers)
        outp_positions.append(simulated_positions)
    return outp_positions


def simulate_knockout_stage(knockout: KnockoutStage, n: int):
    num_teams = len(knockout.teams)
    num_rounds = ceil(log2(num_teams))
    advancement_counts = {team: [0] * (num_rounds + 1) for team in knockout.teams}

    for _ in range(n):
        knockout_stage = knockout.copy()
        results = predict_knockout(knockout_stage)

        rounds = results.rounds
        for team in results.teams:
            advancement_counts[team][0] += 1
        for i in range(len(rounds)):
            print(f"{rounds[i] = }")
            for match in rounds[i]:
                advancement_counts[match.winner][i+1] += 1
    return advancement_counts
