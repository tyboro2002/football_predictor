class Team:
    def __init__(self, name):
        self.name = name
        self.position_prev_season = 0  # The position this team was at in the previous season 0 if it did not play
        self.previous_matches = []

    def add_match(self, match):
        self.previous_matches.append(match)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

