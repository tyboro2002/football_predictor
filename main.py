import math

from models.formats import League
from models.game import check_match_list
from predict import predict_league
from simulate import simulate_league
from visualize import sort_teams_on_metrics, visualize_position_chances, visualize_league, visualize_league_matches, visualize_all_team_matches
from parser import parse_match_list
import time
import pandas as pd

save_location = "results/league_probabilities.png"
save_location2 = "results/league1.png"
match_list_location = "input_data/matches.csv"
amount_of_simulations = 100


def get_matchday_location(day):
    return f"results/matchdays/matchday_{day}.png"


def get_team_location(team_name):
    return f"results/teams/{team_name}.png"


def get_metric_sort_location(metric):
    return f"results/league_metrics/{metric}.csv"


# year              clubs in 1A
# 2023/24 - heden   16
# 2022/23 - 2020/21 18
# 2019/20 - 2009/10 16
# 2008/09 - 1976/77 18
# 1975/76 - 19
# 1974/75 - 20
# 1973/74 - 16

JPL = League(
    [
        ("Club brugge", (
            1, 4, 1, 1, 1, 2, 1, 2, 1, 2, 3, 3, 2, 4, 3, 3, 3, 6, 3, 1, 2, 1, 2, 2, 2, 2, 1, 2, 1, 3, 2, 6, 1, 4, 1, 4,
            1, 3, 2, 2, 3, 5, 15, 6, 1, 6, 1, 1, 1, 4, 5, 1, 2, 2, 2, 5, 2, 2, 5, 9)),  # 1964/65 is the last year
        ("Union", (2, 3, 2, 18 + 1, 16 + 4, 16 + 3, 16 + 6, 16 + 4, 16 + 6)),  # 2015/16 is the last year
        ("Anderlecht", (
            3, 11, 3, 4, 8, 6, 3, 1, 2, 3, 1, 1, 1, 3, 1, 2, 2, 1, 1, 2, 1, 2, 3, 1, 1, 3, 4, 4, 2, 1, 1, 1, 2, 1, 2, 2,
            4, 1, 1, 1, 2, 2, 2, 1, 5, 2, 2, 2, 2, 3, 1, 6, 1, 3, 4, 4, 1, 1, 1, 1)),  # 1964/65 is the last year
        ("Cercle brugge", (
            4, 8, 10, 16, 14, 13, 16 + 1, 16 + 6, 16 + 5, 15, 11, 16, 7, 9, 9, 9, 4, 12, 14, 11, 14, 11, 14, 18 + 1,
            18 + 6, 18 + 7,
            18 + 8, 18 + 9, 18 + 10, 18, 8, 15, 12, 13, 9, 16, 9, 15, 7, 11, 10, 11, 11, 12, 14, 14, 10, 18 + 1, 17, 8,
            13, 10,
            8, 11, 5, 16 + 11, 16 + 6, 16 + 4)),  # 1968/69 is the last year
        ("Krc genk", (
            5, 2, 8, 2, 7, 1, 5, 8, 4, 7, 6, 5, 3, 1, 11, 8, 10, 2, 5, 3, 4, 6, 1, 11, 8, 1, 2, 8, 18 + 2, 18 + 3, 18,
            15,
            16, 14, 18 + 4, 18)),  # 1988/89 is the last year
        ("Antwerpen", (
            6, 1, 4, 3, 4, 4, 8, 16 + 3, 16 + 3, 16 + 10, 16 + 7, 16 + 10, 16 + 10, 16 + 6, 16 + 8, 18 + 3, 18 + 5,
            18 + 4, 18 + 7, 18 + 4, 18,
            12, 16, 12, 18 + 1, 18 + 2, 18, 6, 13, 16, 5, 5, 5, 7, 4, 5, 3, 14, 9, 7, 8, 3, 5, 9, 13, 7, 8, 7, 11, 2, 2,
            7,
            12, 13, 16 + 2, 16 + 12, 15, 5, 10, 13)),  # 1964/65 is the last year
        ("Gent", (
            7, 5, 5, 7, 2, 5, 4, 3, 3, 1, 7, 12, 4, 5, 2, 4, 6, 4, 4, 6, 9, 8, 4, 5, 3, 8, 8, 14, 14, 14, 15, 9, 6, 3,
            6, 18 + 2, 17, 16, 4, 6, 15, 4, 3, 10, 18 + 1, 18 + 3, 18 + 4, 18 + 8, 19 + 12, 20 + 16 + 1, 16 + 10,
            16 + 10, 16 + 8, 16, 3, 11,
            16 + 1, 15, 7, 12)),  # 1964/65 is the last year
        ("Kv mechelen", (
            8, 13, 7, 8, 6, 16 + 1, 16, 7, 10, 9, 13, 8, 9, 7, 7, 10, 13, 18 + 2, 18 + 13, 18 + 18 + 1, 18 + 18 + 7, 17,
            18 + 1, 18, 11,
            18 + 1, 18 + 5, 17, 10, 11, 8, 3, 4, 2, 3, 1, 2, 2, 11, 12, 6, 18 + 1, 18, 18 + 5, 18 + 11, 18 + 10, 18 + 7,
            17, 15, 17,
            7, 5, 6, 16 + 2, 16 + 9, 15, 14, 12, 6, 16 + 2)),  # 1964/65 is the last year
        ("Stvv", (
            9, 12, 9, 15, 12, 7, 10, 12, 13, 16 + 1, 16 + 3, 16 + 4, 16, 12, 4, 18 + 1, 17, 15, 15, 14, 13, 4, 8, 13,
            13, 9, 14,
            11, 15, 8, 18 + 1, 18 + 7, 18 + 7, 17, 15, 7, 11, 18 + 1, 18 + 11, 18 + 5, 18 + 6, 18 + 6, 18 + 9, 18 + 11,
            18 + 13, 18 + 8, 18 + 12,
            19 + 3, 20 + 8, 16 + 8, 16, 13, 11, 8, 12, 7, 5, 6, 2, 5)),  # 1964/65 is the last year
        ("Oh leuven", (
            10, 10, 11, 11, 16 + 3, 16 + 7, 16 + 2, 16 + 7, 16, 16 + 5, 15, 10, 14, 16 + 1, 16 + 9, 18 + 12, 18 + 3,
            18 + 5, 18 + 6)),  # 2005/06 is the last year
        ("Westerlo", (
            11, 7, 18 + 1, 18 + 4, 16 + 1, 16 + 4, 16 + 7, 16, 15, 11, 16 + 1, 16 + 3, 15, 8, 12, 6, 9, 8, 9, 12, 6, 10,
            14, 8, 6, 12,
            12, 18 + 2, 18 + 12, 18 + 6, 18 + 11)),  # 1993/94 is the last year
        ("Standard", (
            12, 6, 14, 6, 5, 3, 2, 9, 7, 4, 2, 4, 5, 2, 8, 1, 1, 3, 2, 4, 3, 7, 5, 3, 5, 6, 9, 7, 6, 2, 6, 2, 3, 6, 5,
            6, 10, 10, 3, 8, 4, 1, 1, 3, 2, 3, 3, 3, 8, 6, 4, 2, 3, 1, 1, 1, 3, 4, 3, 2)),  # 1964/65 is the last year
        ("Charlerio", (
            13, 9, 6, 13, 3, 9, 6, 5, 8, 5, 10, 11, 16 + 1, 16, 13, 12, 8, 5, 11, 5, 15, 16, 12, 9, 16, 14, 13, 13, 7,
            13,
            4, 7, 13, 8, 14, 11, 8, 7, 12, 18 + 4, 18 + 9, 18 + 10, 18 + 11, 18 + 6, 17, 9, 12, 16, 16, 14, 16 + 14,
            16 + 3, 16 + 3, 15,
            9, 2, 8, 14, 16 + 2, 16 + 12)),  # 1964/65 is the last year
        ("Kv korterijk", (
            14, 14, 13, 14, 11, 8, 7, 10, 9, 6, 8, 9, 6, 10, 5, 14, 18 + 1, 18 + 3, 18 + 5, 18 + 7)
         ),  # 2004/05 is the last year
        ("Rwdm", (15, 18 + 1, 18 + 2, 18 + 6)),  # 2020/21 is the last year
        ("Kas eupen", (
            16, 15, 15, 12, 13, 12, 15, 13, 16 + 2, 16 + 3, 16 + 2, 16 + 9, 16 + 3, 15, 16 + 4, 18 + 14, 18 + 13,
            18 + 7, 18 + 8, 18 + 13,
            18 + 14, 18 + 2))  # 2002/03 is the last year
    ]
)


# print(JPL.get_standings())
# for matchday in JPL.matchdays:
#     print(matchday)

# print(simulate_game(JPL.matchdays[0][0], 10))


if __name__ == '__main__':
    match_data = parse_match_list(match_list_location)
    assert check_match_list(match_data)
    sort_teams_on_metrics(match_data, get_metric_sort_location)
    # print(match_data)
    # print(partition_list_into_matchdays(match_data, 8))

    # start_time = time.time()
    # data = simulate_league(JPL, amount_of_simulations)
    # end_time = time.time()
    #
    # print(f"Multiprocessing simulation time: {end_time - start_time} seconds")
    # print("data", data)
    # visualize_position_chances(data, save_location, JPL)
    # predicted = predict_league(JPL)
    # visualize_league(predicted, save_location2)
    # visualize_league_matches(predicted, get_matchday_location)
    # visualize_all_team_matches(predicted, get_team_location)

# print(predict_league(JPL))
