from models.formats import League, GroupStage, KnockoutStage
from models.game import check_match_list, FootballGame, partition_list_into_matchdays
from predict import predict_league, predict_group_stage, predict_knockout
from settings import prev_position_location, match_list_location, amount_of_simulations, match_list_location_EK, \
    FIXED_SCHEDULE
from simulate import simulate_league, simulate_group_stage, simulate_knockout_stage
from visualize import sort_teams_on_metrics, visualize_position_chances, visualize_league, visualize_league_matches, \
    visualize_all_team_matches, sort_and_divide_df, visualize_group_standings_chanches
from parser import parse_match_list, create_df_from_matchList, parse_prev_positions
import time
import random

save_location = "results/league_probabilities.png"
save_location2 = "results/league1.png"


def print_advancement_counts(advancement_counts):
    for team, round_counts in advancement_counts.items():
        print(f"Team: {team}")
        print(f"Rounds: {round_counts}")
        # for round_number, count in round_counts.items():
        #     print(f"  Round {round_number + 1}: {count} times")


def get_group_location(group):
    return f"results/group_{chr(65 + group)}_probabilities.png"


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

def generate_season_string(start_year, num_seasons):
    seasons = []
    for i in range(num_seasons):
        current_year = start_year - i
        next_year = current_year + 1
        season = f"{str(current_year)}/{str(next_year)[-2:]}"
        seasons.append(season)
    return ", ".join(seasons)


JPL = League(
    [
        "Club brugge",
        "Union",
        "Anderlecht",
        "Cercle brugge",
        "Krc genk",
        "Antwerpen",
        "Gent",
        "Kv mechelen",
        "Stvv",
        "Oh leuven",
        "Westerlo",
        "Standard",
        "Charleroi",
        "Kv korterijk",
        "Rwdm",
        "Kas eupen"
    ],
    parse_prev_positions(prev_position_location),
    parse_match_list(match_list_location),
    True
)


EK = GroupStage(
    [
        ["Germany", "Scotland", "Hungary", "Switserland"],
        ["Spain", "Croatia", "Italy", "Albania"],
        ["Slovenia", "Denmark", "Serbia", "England"],
        ["Poland", "Netherlands", "Austria", "France"],
        ["Belgium", "Slovakia", "Romania", "Ukrain"],
        ["Turkey", "Georgia", "Portugal", " Tsjechie"]
    ],
    parse_prev_positions(prev_position_location),
    parse_match_list(match_list_location_EK),
    False
)


# print(JPL.get_standings())
# for matchday in JPL.matchdays:
#     print(matchday)

# print(simulate_game(JPL.matchdays[0][0], 10))


if __name__ == '__main__':
    match_data = parse_match_list(match_list_location)
    print(len(match_data))
    assert check_match_list(match_data)
    df = create_df_from_matchList(match_data)
    # print(sort_and_divide_df(
    #     df, "goals_difference", additional_columns=["opponent", "goals_scored", "goals_conceded"]
    # ))
    sort_teams_on_metrics(df, get_metric_sort_location)
    # print(match_data)
    # print(partition_list_into_matchdays(match_data, 8))

    # start_time = time.time()
    # data = simulate_league(JPL, amount_of_simulations)
    # end_time = time.time()
    #
    # print(f"Multiprocessing simulation time: {end_time - start_time} seconds")
    # print("data", data)

    # start_time_EK = time.time()
    # data_EK = simulate_group_stage(EK, amount_of_simulations)
    # end_time_EK = time.time()
    #
    # print(f"Multiprocessing simulation time: {end_time_EK - start_time_EK} seconds")
    # print("data", data_EK)

    predicted_groups = predict_group_stage(EK)
    print(predicted_groups)

    # visualize_group_standings_chanches(data_EK, get_group_location, EK)

    qualified_teams = [team.name for team in predicted_groups.get_qualifying_team_by_position()]
    knockout_stage = KnockoutStage(qualified_teams, FIXED_SCHEDULE)

    simulated = simulate_knockout_stage(knockout_stage, amount_of_simulations)

    print_advancement_counts(simulated)

    predicted_knockout = predict_knockout(knockout_stage)
    print(predicted_knockout)

    # visualize_position_chances(data, save_location, JPL)
    # predicted = predict_league(JPL)
    # print("predicted matches", predicted.matchdays)
    # print(predicted)
    # print(predicted.get_team_by_position(15))
    # # visualize_league(predicted, save_location2)
    # visualize_league_matches(predicted, get_matchday_location)
    # visualize_all_team_matches(predicted, get_team_location)

# print(predict_league(JPL))
