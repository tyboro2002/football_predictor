def partition_list_into_matchdays(input_match_list, matches_per_matchday):
    return [input_match_list[i:i + matches_per_matchday] for i in range(0, len(input_match_list), matches_per_matchday)]


def check_match_list(matches):
    for match in matches:
        if match.home_substitute > 5 or match.away_substitute > 5:
            print(match)
            return False
        if match.ball_possession_home_team > 100:
            print(match)
            return False
        metrics = [
            "home_score",
            "away_score",
            "ball_possession_home_team",
            "home_shots_on_target",
            "away_shots_on_target",
            "home_shots_wide_of_target",
            "away_shots_wide_of_target",
            "home_corners",
            "away_corners",
            "home_free_kicks",
            "away_free_kicks",
            "home_offside",
            "away_offside",
            "home_fouls",
            "away_fouls",
            "home_yellow_cards",
            "away_yellow_cards",
            "home_red_cards",
            "away_red_cards",
            "home_penalty",
            "away_penalty",
            "home_penalty_missed",
            "away_penalty_missed",
            "home_goal_denied",
            "away_goal_denied",
            "home_substitute",
            "away_substitute",
            "home_own_goal",
            "away_own_goal",
            "first_half_extra_time",
            "second_half_extra_time",
        ]
        for metric in metrics:
            if getattr(match, metric) < 0:
                print("value below 0")
                return False
    return True


class FootballGame:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, home, away):
        self.home = home
        self.away = away
        self.home_score = None
        self.away_score = None
        # self.time_elapsed = 0  # in minutes
        # self.game_over = False
        self.ball_possession_home_team = 0
        self.home_shots_on_target = 0
        self.away_shots_on_target = 0
        self.home_shots_wide_of_target = 0
        self.away_shots_wide_of_target = 0
        self.home_corners = 0
        self.away_corners = 0
        self.home_free_kicks = 0
        self.away_free_kicks = 0
        self.home_offside = 0
        self.away_offside = 0
        self.home_fouls = 0
        self.away_fouls = 0
        self.home_yellow_cards = 0
        self.away_yellow_cards = 0
        self.home_red_cards = 0
        self.away_red_cards = 0
        self.home_penalty = 0
        self.away_penalty = 0
        self.home_penalty_missed = 0
        self.away_penalty_missed = 0
        self.home_goal_denied = 0
        self.away_goal_denied = 0
        self.home_substitute = 0
        self.away_substitute = 0
        self.home_own_goal = 0
        self.away_own_goal = 0
        self.first_half_extra_time = 0
        self.second_half_extra_time = 0

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
