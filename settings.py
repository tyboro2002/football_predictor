match_list_location = "input_data/matches.csv"
prev_position_location = "input_data/prev_positions.csv"

# EK
match_list_location_EK = "input_data/matches_EK_group.csv"

amount_of_simulations = 100

WIN_POINTS = 3
DRAW_POINTS = 1
LOSE_POINTS = 0

DECAY_RATE = 0.3
YEARS_BACK = 5

DEFAULT_POSITION = None  # the position if the team is not known in previous seasons

# Fixed schedule where winners of match 0 play against winners of match 1, and so on
FIXED_SCHEDULE = [
    [(0, 1), (2, 3), (4, 5), (6, 7), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16)],
    [(0, 1), (2, 3), (4, 5), (6, 7)],
    [(0, 1), (2, 3)],  # Round 2 (Quarterfinals)
    [(0, 1)]  # Round 3 (Semifinals)
]
