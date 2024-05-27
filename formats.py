import game
import random
import itertools
from game import FootballGame


def generate_all_matches(League):
    matches = []
    for team1, team2 in itertools.combinations(League.teams, 2):
        matches.append(FootballGame(team1, team2))  # team1 plays at home
        matches.append(FootballGame(team2, team1))  # team2 plays at home
    return matches


def check_leauge(League, schedule):
    needed_matches = generate_all_matches(League)
    toplay = {team: [t for t in League.teams if t != team] for team in League.teams}
    for matchday in schedule:
        already_played = []
        for match in matchday:
            if match.team1 in already_played or match.team2 in already_played or match not in needed_matches or match.team2 not in toplay[match.team1] or match.team1 not in toplay[match.team2]:
                print("fails at:")
                print(matchday)
                print(needed_matches)
                print(match)
                print("full schedule")
                for matchday in schedule:
                    print(matchday)
                return False
            toplay[match.team1].remove(match.team2)
            toplay[match.team2].remove(match.team1)
            already_played.append(match.team1)
            already_played.append(match.team2)
            needed_matches.remove(match)
        if len(toplay[League.teams[0]]) == 0:
            toplay = {team: [t for t in League.teams if t != team] for team in League.teams}
    return True


def generate_league_match_schedule(League):
    total_teams = len(League.teams)
    total_matchdays = (total_teams - 1) * 2
    matchdays = []
    all_matches = generate_all_matches(League)
    toplay = {team: [t for t in League.teams if t != team] for team in League.teams}

    for i in range(total_matchdays):
        matchday = []
        matchday_to_play = list(League.teams)
        while len(matchday_to_play) > 0:
            choosen = random.choice(matchday_to_play)
            match: [FootballGame] = random.choice([
                match for match in
                all_matches if
                (match.team1 == choosen or match.team2 == choosen) and
                match.team2 in matchday_to_play and match.team1 in matchday_to_play
                and match.team2 in toplay[match.team1]
                and match.team1 in toplay[match.team2]
            ])
            all_matches.remove(match)
            matchday_to_play.remove(match.team1)
            matchday_to_play.remove(match.team2)
            toplay[match.team1].remove(match.team2)
            toplay[match.team2].remove(match.team1)

            matchday.append(match)
        matchdays.append(matchday)
        if len(toplay[League.teams[0]]) == 0:
            toplay = {team: [t for t in League.teams if t != team] for team in League.teams}

    return matchdays
