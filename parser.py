from typing import List

from models.team import Team
from models.game import FootballGame
import pandas as pd


def get_teams_before_class(seasons_back, division):
    a1 = [16, 18, 18, 18, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,
          18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 20, 16, 16, 16, 16,
          16, 16, 16, 16, 16, 16]
    b1 = [16 for _ in range(len(a1))]
    if division == "1B":
        return a1[seasons_back]
    elif division == "3K":
        return b1[seasons_back] + a1[seasons_back]


def parse_match_list(save_location):
    with open(save_location, "r", encoding="utf-8") as file:
        teams = [Team(team_name.strip()) for team_name in file.readline().split(",")]
        titles = [word.strip() for word in file.readline().split(",")]
        lines = [line.strip() for line in file.readlines()]
        matches = []
        for line in lines:
            if not line.startswith("#") and line.strip():
                line = line.split(",")
                match_data = {titles[i]: line[i].strip() for i in range(len(titles))}
                home_team = teams[int(match_data['home_team'])]
                away_team = teams[int(match_data['away_team'])]
                match = FootballGame(home_team, away_team)
                for key, value in match_data.items():
                    if key not in ['home_team', 'away_team']:
                        setattr(match, key, int(value))
                matches.append(match)

        return matches


def create_df_from_matchList(matches: List[FootballGame]):
    # Initialize a list to hold team data
    team_data = []

    # Iterate through matches and extract team details
    for match in matches:
        # Team 1 details
        team_data.append({
            "team": match.home,
            "opponent": match.away,
            "goals_scored": match.home_score,
            "goals_conceded": match.away_score,
            "goals_difference": match.home_score - match.away_score,
            "possession": match.ball_possession_home_team,
            "possession_conceded": 100 - match.ball_possession_home_team,
            "shots_on_target": match.home_shots_on_target,
            "shots_on_target_conceded": match.away_shots_on_target,
            "shots_wide_of_target": match.home_shots_wide_of_target,
            "shots_wide_of_target_conceded": match.away_shots_wide_of_target,
            "corners": match.home_corners,
            "corners_conceded": match.away_corners,
            "free_kicks": match.home_free_kicks,
            "free_kicks_conceded": match.away_free_kicks,
            "offside": match.home_offside,
            "offside_conceded": match.away_offside,
            "fouls": match.home_fouls,
            "fouls_conceded": match.away_fouls,
            "yellow_cards": match.home_yellow_card,
            "yellow_cards_opponent": match.away_yellow_cards,
            "red_cards": match.home_red_cards,
            "red_cards_opponent": match.away_red_cards,
            "penalty": match.home_penalty,
            "penalty_conceded": match.away_penalty,
            "penalty_missed": match.home_penalty_missed,
            "penalty_stopped": match.away_penalty_missed,
            "goal_denied": match.home_goal_denied,
            "goal_denied_opponent": match.away_goal_denied,
            "substitute": match.home_substitute,
            "substitute_opponent": match.away_substitute,
            "own_goal_opponent": match.home_own_goal,
            "own_goal_self": match.away_own_goal,
            "first_half_extra": match.first_half_extra_time,
            "second_half_extra": match.second_half_extra_time,
            "play_time": 90 + match.first_half_extra_time + match.second_half_extra_time
        })
        # Team 2 details
        team_data.append({
            "team": match.away,
            "opponent": match.home,
            "goals_scored": match.away_score,
            "goals_conceded": match.home_score,
            "goals_difference": match.away_score - match.home_score,
            "possession": 100 - match.ball_possession_home_team,
            "possession_conceded": match.ball_possession_home_team,
            "shots_on_target": match.away_shots_on_target,
            "shots_on_target_conceded": match.home_shots_on_target,
            "shots_wide_of_target": match.away_shots_wide_of_target,
            "shots_wide_of_target_conceded": match.home_shots_wide_of_target,
            "corners": match.away_corners,
            "corners_conceded": match.home_corners,
            "free_kicks": match.away_free_kicks,
            "free_kicks_conceded": match.home_free_kicks,
            "offside": match.away_offside,
            "offside_conceded": match.home_offside,
            "fouls": match.away_fouls,
            "fouls_conceded": match.home_fouls,
            "yellow_cards": match.away_yellow_cards,
            "yellow_cards_opponent": match.home_yellow_card,
            "red_cards": match.away_red_cards,
            "red_cards_opponent": match.home_red_cards,
            "penalty": match.away_penalty,
            "penalty_conceded": match.home_penalty,
            "penalty_missed": match.away_penalty_missed,
            "penalty_stopped": match.home_penalty_missed,
            "goal_denied": match.away_goal_denied,
            "goal_denied_opponent": match.home_goal_denied,
            "substitute": match.away_substitute,
            "substitute_opponent": match.home_substitute,
            "own_goal_opponent": match.away_own_goal,
            "own_goal_self": match.home_own_goal,
            "first_half_extra": match.first_half_extra_time,
            "second_half_extra": match.second_half_extra_time,
            "play_time": 90 + match.first_half_extra_time + match.second_half_extra_time
        })

    # Create a DataFrame from the team data
    df = pd.DataFrame(team_data)
    return df


def replace_value(value, col_index, division):
    # Extract the identifier (should be "1B" always in this case)
    identifier = value.split()[1]
    # Get the result from get_teams
    return get_teams_before_class(col_index, division) + int(identifier)


def parse_prev_positions(save_location):
    df = pd.read_csv(save_location, dtype=str)

    # Trim whitespace from each value in the DataFrame
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    for col in df.columns:
        col_index = df.columns.get_loc(col)

        df[col] = df[col].apply(
            lambda x: replace_value(x, col_index - 1, "1B") if str(x).startswith("1B") else x)
        df[col] = df[col].apply(
            lambda x: replace_value(x, col_index - 1, "3K") if str(x).startswith("3K") else x)
    return df
