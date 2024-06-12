from typing import List

from settings import WIN_POINTS, DRAW_POINTS, LOSE_POINTS, DECAY_RATE, YEARS_BACK, DEFAULT_POSITION
from models.game import FootballGame, partition_list_into_matchdays
from models.team import Team
from copy import deepcopy
import random
import itertools
import pandas as pd
import numpy as np


def generate_all_possible_orders(teams):
    return list(itertools.permutations(teams))


def can_place_teams_in_order(formated, teams, best, order):
    """
    Tries to place the teams in the given order in the 'formated' list.

    Parameters:
    - formated: List of positions (strings and lists of group letters).
    - teams: List of tuples (team_name, group_letter).
    - best: The nth best teams to place.
    - order: A permutation of teams to try placing in the formated positions.

    Returns:
    - A list of placements if successful, otherwise None.
    """
    formated_copy = formated[:]

    for team, group in order:
        placed = False
        for i in range(len(formated_copy)):
            if isinstance(formated_copy[i], list) and group in formated_copy[i]:
                formated_copy[i] = f'{best}{group}'
                placed = True
                break
        if not placed:
            return None  # Could not place this team

    return formated_copy


def try_all_possible_orders(formated, teams, best):
    """
    Generates all possible valid orders of team placements.

    Parameters:
    - formated: List of positions (strings and lists of group letters).
    - teams: List of tuples (team_name, group_letter).
    - best: The nth best teams to place.

    Returns:
    - A list of valid placements.
    """
    all_orders = list(itertools.permutations(teams))

    for order in all_orders:
        placement = can_place_teams_in_order(formated, teams, best, order)
        if placement is not None:
            return placement

    raise ValueError('No valid placements found')


class KnockoutStage:
    def __init__(self, teams: List[str], fixed_schedule=None):
        if len(teams) % 2 != 0:
            raise ValueError("The number of teams must be even.")

        self.teams = [Team(team) for team in teams]
        self.rounds = []
        self.current_round = []
        self.fixed_schedule = fixed_schedule
        self.setup_initial_matchups()

    def copy(self):
        return KnockoutStage([team.name for team in self.teams], self.fixed_schedule)

    def setup_initial_matchups(self):
        random.shuffle(self.teams)
        self.current_round = [FootballGame(self.teams[i], self.teams[i + 1]) for i in range(0, len(self.teams), 2)]
        self.rounds.append(self.current_round)

    def record_match_result(self, *args):
        if args[0] is not None and isinstance(args[0], FootballGame):
            game = args[0]
            home_team = game.home
            away_team = game.away
            home_goals = game.home_score
            away_goals = game.away_score
        else:
            home_team, away_team, home_goals, away_goals = args

        if home_goals > away_goals:
            winner = home_team
        else:
            winner = away_team

        game.winner = winner

    def progress_to_next_round(self):
        winners = [game.winner for game in self.current_round if hasattr(game, 'winner')]
        if len(winners) % 2 != 0:
            raise ValueError("Number of winners must be even to form new matchups.")

        self.current_round = []
        if self.fixed_schedule:
            for matchup in self.fixed_schedule[len(self.rounds)]:
                team1 = winners[matchup[0]]
                team2 = winners[matchup[1]]
                self.current_round.append(FootballGame(team1, team2))
        else:
            self.current_round = [FootballGame(winners[i], winners[i + 1]) for i in range(0, len(winners), 2)]

        self.rounds.append(self.current_round)

    def get_bracket(self):
        bracket = []
        for rnd in self.rounds:
            round_results = []
            for game in rnd:
                result = f"{game.home.name} vs {game.away.name}"
                if hasattr(game, 'winner'):
                    result += f" - Winner: {game.winner.name}"
                round_results.append(result)
            bracket.append(round_results)
        return bracket

    def __str__(self):
        bracket = self.get_bracket()
        result = []
        for i, round_results in enumerate(bracket):
            if len(round_results) != 1:
                result.append(f"Round {i + 1}: 1/{len(round_results)} final:")
            else:
                result.append(f"Round {i + 1}: final:")
            result.extend(round_results)
            result.append("")
        return "\n".join(result)


class GroupStage:
    def __init__(self, groups, prev_positions_df, matchdays=None, keep_scores=False, matches_per_group=6):
        self.groups = groups
        self.leagues = []
        if matchdays is not None and not isinstance(matchdays[0], list):
            matchdays = partition_list_into_matchdays(matchdays, matches_per_group)
        for i in range(len(groups)):
            group_teams = groups[i]
            group_matchdays = matchdays[i] if matchdays is not None else None
            league = League(group_teams, prev_positions_df, matchdays=group_matchdays, keep_scores=keep_scores)
            self.leagues.append(league)

    def record_match_result(self, group_idx, *args):
        self.leagues[group_idx].record_match_result(*args)

    def get_standings(self):
        return {f"Group {chr(65 + i)}": league.get_standings() for i, league in enumerate(self.leagues)}

    def generate_group_stage_match_schedule(self):
        matchdays = []
        for league in self.leagues:
            matchdays.extend(league.generate_league_match_schedule())
        return matchdays

    def __str__(self):
        result = ""
        for i, league in enumerate(self.leagues):
            result += f"Group {chr(65 + i)} Standings:\n"
            result += str(league) + "\n\n"
        return result

    def get_team_by_position(self, position):
        """
        Get the team at a specific position within a group.

        Parameters:
        - position: A string in the format '1A', '2B', etc., where the number indicates the position and the letter indicates the group.

        Returns:
        - The team name at the specified position.
        """
        pos = int(position[0]) - 1  # Convert position to zero-based index
        group = ord(position[1].upper()) - ord("A")  # Get the group index
        if group < len(self.leagues) and pos < len(self.leagues[group].teams):
            return self.leagues[group].get_team_by_position(pos)
        else:
            if group < len(self.leagues):
                raise ValueError(f"Invalid group: {group}")
            if pos < len(self.leagues[group].teams):
                raise ValueError(f"Invalid position: {position}")

    def get_x_best_nth_placed_teams(self, amount_of_teams, place):
        teams_names = {}
        teams = []
        for i in range(len(self.leagues)):
            league = self.leagues[i]
            teams_names[league.get_standings()[place-1][0]] = chr(65+i)
            teams.append(league.get_standings()[place - 1])

        return ([(item[0], teams_names[item[0]]) for item in sorted(teams,
               key=lambda item: (
                   item[1]["points"], item[1]["won"], item[1]["scored"] - item[1]["conceded"],
                   item[1]["scored"]),
               reverse=True)][:amount_of_teams])

    def get_qualifying_team_by_position(self, positions=None):
        if positions is None:
            positions = ["2A", "2B", "1A", "2C", "1C", "3D/E/F", "1B", "3A/D/E/F", "2D", "2E", "1F", "3A/B/C", "1E", "3A/B/C/D", "1D", "2F"]

        formated = []
        best = None
        best_amount = 0
        for position in positions:
            if "/" in position:
                best = int(position[0])
                best_amount += 1
                formated.append([group for group in position[1:].split("/")])
            else:
                formated.append(position)

        if best is not None:
            teams = self.get_x_best_nth_placed_teams(best_amount, best)
            formated = try_all_possible_orders(formated, teams, best)
            # print(teams)
            # for team in teams:
            #     for i in range(len(formated)):
            #         print(formated[i], team[1])
            #         if isinstance(formated[i], list) and team[1] in formated[i]:
            #             formated[i] = str(best) + team[1]
            #             break

        output = []
        for position in formated:
            output.append(self.get_team_by_position(position))
        return output


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

        teams = [team.strip() for team in teams]

        self.teams = [Team(team) for team in teams]
        self.standings = {
            team: {"played": 0, "won": 0, "drawn": 0, "lost": 0, "points": 0, "scored": 0, "conceded": 0}
            for team in self.teams}

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

        self.prev_standings = {row.iloc[0]: calculate_position_factor(row.iloc[1:].tolist()) for _, row in
                               prev_positions_df.iterrows()}

        if self.prev_standings is not None:
            for team in self.teams:
                team.position_prev_season = self.prev_standings.get(team.name, DEFAULT_POSITION)
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

        if home_goals > away_goals:
            self.standings[home_team]["won"] += 1
            self.standings[away_team]["lost"] += 1
            self.standings[home_team]["points"] += WIN_POINTS
            self.standings[away_team]["points"] += LOSE_POINTS
        elif away_goals > home_goals:
            self.standings[away_team]["won"] += 1
            self.standings[home_team]["lost"] += 1
            self.standings[away_team]["points"] += WIN_POINTS
            self.standings[home_team]["points"] += LOSE_POINTS
        else:
            self.standings[home_team]["drawn"] += 1
            self.standings[away_team]["drawn"] += 1
            self.standings[home_team]["points"] += DRAW_POINTS
            self.standings[away_team]["points"] += DRAW_POINTS

        self.standings[home_team]["scored"] += home_goals
        self.standings[home_team]["conceded"] += away_goals
        self.standings[away_team]["scored"] += away_goals
        self.standings[away_team]["conceded"] += home_goals
        self.standings[home_team]["played"] += 1
        self.standings[away_team]["played"] += 1

    def get_standings(self):
        return sorted(self.standings.items(),
                      key=lambda item: (
                          item[1]["points"], item[1]["won"], item[1]["scored"] - item[1]["conceded"],
                          item[1]["scored"]),
                      reverse=True)

    def get_team_by_position(self, position):
        """
        Get the team at a specific position within a leauge.

        Parameters:
        - position: A integer., where the number indicates the position.

        Returns:
        - The team at the specified position.
        """
        if position < len(self.teams):
            return sorted(self.standings.items(),
                          key=lambda item: (
                              item[1]["points"], item[1]["won"], item[1]["scored"] - item[1]["conceded"],
                              item[1]["scored"]),
                          reverse=True)[position][0]
        else:
            raise ValueError(f"Invalid position: {position}")

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
                    print("\n")
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
