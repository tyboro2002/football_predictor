from settings import WIN_POINTS, DRAW_POINTS, LOSE_POINTS, DECAY_RATE, YEARS_BACK
from models.game import FootballGame, partition_list_into_matchdays
from models.team import Team
from copy import deepcopy
import random
import itertools
import pandas as pd
import numpy as np


class League:
    def __init__(self, teams, prev_positions_df, matchdays=None, keep_scores=False):
        if len(teams) % 2 != 0:
            raise ValueError("The number of teams must be even.")

        def calculate_position_factor(positions, decay_rate=DECAY_RATE):
            """
            Calculate the position factor, applying a decay rate to older years.

            Parameters:
            - positions: List of positions or "DNP".
            - decay_rate: The rate at which older years are reduced. A value between 0 and 1.

            Returns:
            - The weighted mean of the positions.
            """
            # Trim positions at the first NaN
            valid_positions = positions[:YEARS_BACK]

            # Convert 'DNP' to middle position
            valid_positions = np.where(valid_positions == 'DNP', len(valid_positions) / 2, valid_positions)

            # Convert to float
            valid_positions = valid_positions.astype(float)

            # Calculate decay weights
            weights = np.array([decay_rate ** i for i in range(len(valid_positions))])[::-1]

            # Calculate weighted average
            weighted_sum = np.sum(valid_positions * weights)
            return weighted_sum / np.sum(weights)

        self.prev_positions_df = prev_positions_df
        self.keep_scores = keep_scores
        self.teams = [Team(team) for team in teams]
        self.standings = {
            team: {"played": 0, "won": 0, "drawn": 0, "lost": 0, "points": 0, "scored": 0, "conceded": 0}
            for team in teams}
        # set the matchdays
        if matchdays is not None:
            if not isinstance(matchdays[0], list):
                matchdays = partition_list_into_matchdays(matchdays, len(teams) // 2)
            if keep_scores:
                self.matchdays = matchdays
                for matchday in matchdays:
                    for match in matchday:
                        self.record_match_result(match)
            else:
                new_matchdays = []
                for matchday in matchdays:
                    new_matchday = []
                    for match in matchday:
                        # Create a new match with the same home and away teams but no scores
                        new_match = FootballGame(match.home, match.away)
                        new_matchday.append(new_match)
                    new_matchdays.append(new_matchday)
                self.matchdays = new_matchdays
        else:
            self.matchdays = self.generate_league_match_schedule()

        self.prev_standings = {row.iloc[0]: calculate_position_factor(row.iloc[1:].tolist()) for _, row in prev_positions_df.iterrows()}

        if self.prev_standings is not None:
            for team in self.teams:
                team.position_prev_season = self.prev_standings[team.name]
        assert self.check_leauge(self.matchdays)

    def record_match_result(self, *args):
        if args[0] is not None and isinstance(args[0], FootballGame):
            game = args[0]
            home_team = game.home
            away_team = game.away
            home_goals = game.home_score
            away_goals = game.away_score
        else:
            home_team, away_team, home_goals, away_goals = args

        home_name = home_team.name
        away_name = away_team.name

        if home_goals > away_goals:
            self.standings[home_name]["won"] += 1
            self.standings[away_name]["lost"] += 1
            self.standings[home_name]["points"] += WIN_POINTS
            self.standings[away_name]["points"] += LOSE_POINTS
        elif away_goals > home_goals:
            self.standings[away_name]["won"] += 1
            self.standings[home_name]["lost"] += 1
            self.standings[away_name]["points"] += WIN_POINTS
            self.standings[home_name]["points"] += LOSE_POINTS
        else:
            self.standings[home_name]["drawn"] += 1
            self.standings[away_name]["drawn"] += 1
            self.standings[home_name]["points"] += DRAW_POINTS
            self.standings[away_name]["points"] += DRAW_POINTS

        self.standings[home_name]["scored"] += home_goals
        self.standings[home_name]["conceded"] += away_goals
        self.standings[away_name]["scored"] += away_goals
        self.standings[away_name]["conceded"] += home_goals
        self.standings[home_name]["played"] += 1
        self.standings[away_name]["played"] += 1

    def get_standings(self):
        return sorted(self.standings.items(),
                      key=lambda item: (item[1]["points"], item[1]["won"], item[1]["scored"] - item[1]["conceded"], item[1]["scored"]),
                      reverse=True)

    def set_matchdays(self, matchdays):
        self.matchdays = matchdays

    def __str__(self):
        standings = self.get_standings()
        data = []
        for team, stats in standings:
            gd = stats['scored'] - stats['conceded']
            data.append(
                [team, stats['played'], stats['won'], stats['drawn'], stats['lost'], stats['scored'], stats['conceded'],
                 gd, stats['points']])

        df = pd.DataFrame(data,
                          columns=["Team", "Played", "Won", "Drawn", "Lost", "Scored", "Conceded", "GD", "Points"])
        return df.to_string(index=False)

    def copy(self):
        new_league = League(
            [team.name for team in self.teams], self.prev_positions_df, None, self.keep_scores)
        new_league.standings = deepcopy(self.standings)
        new_league.matchdays = deepcopy(self.matchdays)
        return new_league

    def generate_all_matches(self):
        matches = []
        for team1, team2 in itertools.combinations(self.teams, 2):
            matches.append(FootballGame(team1, team2))  # team1 plays at home
            matches.append(FootballGame(team2, team1))  # team2 plays at home
        return matches

    def check_leauge(self, schedule):
        needed_matches = self.generate_all_matches()
        toplay = {team: [t for t in self.teams if t != team] for team in self.teams}
        for matchday in schedule:
            already_played = []
            for match in matchday:
                if match.home in already_played or match.away in already_played or match not in needed_matches or match.away not in \
                        toplay[match.home] or match.home not in toplay[match.away]:
                    if match.home in already_played or match.away in already_played:
                        print("Already played")
                    if match not in needed_matches:
                        print("already played match")
                    if match.away not in toplay[match.home] or match.home not in toplay[match.away]:
                        print("not toplay")
                    print("fails at:")
                    print(matchday)
                    print(needed_matches)
                    print(match)
                    print("full schedule")
                    for matchday in schedule:
                        print(matchday)
                    return False
                toplay[match.home].remove(match.away)
                toplay[match.away].remove(match.home)
                already_played.append(match.home)
                already_played.append(match.away)
                needed_matches.remove(match)
            if len(toplay[self.teams[0]]) == 0:
                toplay = {team: [t for t in self.teams if t != team] for team in self.teams}
        return True

    def generate_league_match_schedule(self, max_retries=10_000):
        retrys = 0
        total_teams = len(self.teams)
        total_matchdays = (total_teams - 1) * 2
        while True:
            try:
                matchdays = []
                all_matches = self.generate_all_matches()
                toplay = {team: [t for t in self.teams if t != team] for team in self.teams}

                for i in range(total_matchdays):
                    matchday = []
                    matchday_to_play = list(self.teams)
                    while len(matchday_to_play) > 0:
                        choosen = min(matchday_to_play,
                                      key=lambda team: len(
                                          self.get_team_possibilities(all_matches, team, matchday_to_play, toplay)))
                        possibilities = self.get_team_possibilities(all_matches, choosen, matchday_to_play, toplay)
                        if len(possibilities) != 0:
                            pass
                        match: [FootballGame] = random.choice(possibilities)
                        all_matches.remove(match)
                        matchday_to_play.remove(match.home)
                        matchday_to_play.remove(match.away)
                        toplay[match.home].remove(match.away)
                        toplay[match.away].remove(match.home)

                        matchday.append(match)
                    matchdays.append(matchday)
                    if len(toplay[self.teams[0]]) == 0:
                        toplay = {team: [t for t in self.teams if t != team] for team in self.teams}

                return matchdays
            except IndexError:
                retrys += 1
                if retrys >= max_retries:
                    raise RuntimeError("Failed to generate a valid schedule within the maximum number of retries")

    def get_team_possibilities(self, all_matches, team, matchday_to_play, toplay):
        # return [match for match in all_matches if (match.home == team or match.away == team)]
        return [match for match in
                all_matches if
                (match.home == team or match.away == team) and
                match.away in matchday_to_play and match.home in matchday_to_play
                and match.away in toplay[match.home]
                and match.home in toplay[match.away]
                ]
