from settings import WIN_POINTS, DRAW_POINTS, LOSE_POINTS
class League:
    def __init__(self, teams):
        if len(teams) % 2 != 0:
            raise ValueError("The number of teams must be even.")

        self.teams = teams
        self.matchdays = None
        self.standings = {team: {"played": 0, "won": 0, "drawn": 0, "lost": 0, "points": 0} for team in teams}

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

        self.standings[home_team]["played"] += 1
        self.standings[away_team]["played"] += 1

    def get_standings(self):
        return sorted(self.standings.items(), key=lambda item: item[1]["points"], reverse=True)

    def set_matchdays(self, matchdays):
        self.matchdays = matchdays

    def __str__(self):
        standings = self.get_standings()
        table = "Team\t\tPlayed\tWon\tDrawn\tLost\tPoints\n"
        for team, stats in standings:
            table += (f"{team}\t\t{stats['played']}\t {stats['won']}\t  {stats['drawn']}\t     "
                      f"{stats['lost']}     \t{stats['points']}\n")
        return table


class FootballGame:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.score1 = 0
        self.score2 = 0
        self.time_elapsed = 0  # in minutes
        self.game_over = False
    """
    def update_score(self, team, points):
        if not self.game_over:
            if team == self.team1:
                self.score1 += points
            elif team == self.team2:
                self.score2 += points
            else:
                raise ValueError("Team not playing in this game.")
        else:
            raise RuntimeError("Cannot update score. The game is over.")

    def update_time(self, minutes):
        if not self.game_over:
            self.time_elapsed += minutes
            if self.time_elapsed >= 90:  # assuming 90 minutes for a football game
                self.time_elapsed = 90
                self.game_over = True
        else:
            raise RuntimeError("Cannot update time. The game is over.")

    def get_score(self):
        return {self.team1: self.score1, self.team2: self.score2}

    def is_game_over(self):
        return self.game_over
    """

    def __str__(self):
        return (f"{self.team1} vs {self.team2}")
                # f"Score: {self.team1} {self.score1} - {self.team2} {self.score2}\n"
                # f"Time Elapsed: {self.time_elapsed} minutes\n"
                # f"Game Over: {'Yes' if self.game_over else 'No'}")
    def __repr__(self):
        return (f"{self.team1} vs {self.team2}")

    def __eq__(self, other):
        return self.team1 == other.team1 and self.team2 == other.team2