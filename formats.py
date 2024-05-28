from settings import WIN_POINTS, DRAW_POINTS, LOSE_POINTS
from game import FootballGame
from copy import deepcopy
import random
import itertools


class League:
    def __init__(self, teams):
        if len(teams) % 2 != 0:
            raise ValueError("The number of teams must be even.")

        self.teams = teams
        self.standings = {team: {"played": 0, "won": 0, "drawn": 0, "lost": 0, "points": 0, "scored": 0, "conceded": 0}
                          for team in teams}
        self.matchdays = self.generate_league_match_schedule()
        assert self.check_leauge(self.matchdays)

    def record_match_result(self, home_team, away_team, home_goals, away_goals):
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
                      key=lambda item: (item[1]["points"], item[1]["scored"] - item[1]["conceded"], item[1]["scored"]),
                      reverse=True)

    def set_matchdays(self, matchdays):
        self.matchdays = matchdays

    def __str__(self):
        standings = self.get_standings()
        table = "Team\t\tPlayed\tWon\tDrawn\tLost\tScored\tconceded\tGD\tPoints\n"
        for team, stats in standings:
            table += (f"{team}\t\t{stats['played']}\t {stats['won']}\t  {stats['drawn']}\t     "
                      f"{stats['lost']}     \t{stats['scored']}        \t{stats['conceded']}    \t{stats['scored'] - stats['conceded']} \t{stats['points']}\n")
        return table

    def copy(self):
        new_league = League(deepcopy(self.teams))
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

    def generate_league_match_schedule(self):
        total_teams = len(self.teams)
        total_matchdays = (total_teams - 1) * 2
        matchdays = []
        all_matches = self.generate_all_matches()
        toplay = {team: [t for t in self.teams if t != team] for team in self.teams}

        for i in range(total_matchdays):
            matchday = []
            matchday_to_play = list(self.teams)
            while len(matchday_to_play) > 0:
                choosen = random.choice(matchday_to_play)
                match: [FootballGame] = random.choice([
                    match for match in
                    all_matches if
                    (match.home == choosen or match.away == choosen) and
                    match.away in matchday_to_play and match.home in matchday_to_play
                    and match.away in toplay[match.home]
                    and match.home in toplay[match.away]
                ])
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