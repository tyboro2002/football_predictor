class FootballGame:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, home, away):
        self.home = home
        self.away = away
        self.home_score = None
        self.away_score = None
        self.time_elapsed = 0  # in minutes
        self.game_over = False

    """
    def update_score(self, team, points):
        if not self.game_over:
            if team == self.home:
                self.home_score += points
            elif team == self.away:
                self.away_score += points
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
        return {self.home: self.home_score, self.away: self.away_score}

    def is_game_over(self):
        return self.game_over
    """

    def __str__(self):
        if self.home_score is not None:
            return f"{self.home} {self.home_score} - {self.away} {self.away_score}"
        return f"{self.home} vs {self.away}"
        # f"Score: {self.home} {self.home_score} - {self.away} {self.away_score}\n"
        # f"Time Elapsed: {self.time_elapsed} minutes\n"
        # f"Game Over: {'Yes' if self.game_over else 'No'}")

    def __repr__(self):
        if self.home_score is not None:
            return f"{self.home} {self.home_score} - {self.away_score} {self.away}"
        return f"{self.home} vs {self.away}"

    def __eq__(self, other):
        return self.home == other.home and self.away == other.away
