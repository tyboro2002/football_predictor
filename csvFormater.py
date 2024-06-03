inp_file = "input_data/inp.csv"


def askUser():
    # Writing to file
    with open(inp_file, "w") as file:
        writeLast("home_team, away_team, home_score, away_score, ball_possession_home_team, home_shots_on_target, away_shots_on_target, home_shots_wide_of_target, away_shots_wide_of_target, home_corners, away_corners, home_free_kicks, away_free_kicks, home_offside, away_offside, home_fouls, away_fouls, home_yellow_card, away_yellow_cards, home_red_cards, away_red_cards, home_penalty, away_penalty, home_penalty_missed, away_penalty_missed, home_goal_denied, away_goal_denied, home_substitute, away_substitute, home_own_goal, away_own_goal, first_half_extra_time, second_half_extra_time", file)
        while True:
            # Writing data to a file
            ask("home_team", file)  # home_team
            ask("away_team", file)  # away_team
            ask("home_score", file)  # home_score
            ask("away_score", file)  # away_score
            ask("ball_possession_home_team", file)  # ball_possession_home_team
            ask("home_shots_on_target", file)  # home_shots_on_target
            ask("away_shots_on_target", file)  # away_shots_on_target
            ask("home_shots_wide_of_target", file)  # home_shots_wide_of_target
            ask("away_shots_wide_of_target", file)  # away_shots_wide_of_target
            ask("home_corners", file)  # home_corners
            ask("away_corners", file)  # away_corners
            ask("home_free_kicks", file)  # home_free_kicks
            ask("away_free_kicks", file)  # away_free_kicks
            ask("home_offside", file)  # home_offside
            ask("away_offside", file)  # away_offside
            ask("home_fouls", file)  # home_fouls
            ask("away_fouls", file)  # away_fouls

            home_yellow_card = 0
            away_yellow_cards = 0
            home_red_cards = 0
            away_red_cards = 0
            home_penalty = 0
            away_penalty = 0
            home_penalty_missed = 0
            away_penalty_missed = 0
            home_goal_denied = 0
            away_goal_denied = 0
            home_substitute = 0
            away_substitute = 0
            home_own_goal = 0
            away_own_goal = 0
            first_half_extra = 0
            second_half_extra = 0
            first_half_over = False

            while True:
                code = input("Enter code (or 'END' to finish): ").strip().upper()
                if code == "END":
                    break
                elif code == "HY":
                    home_yellow_card += 1
                elif code == "AY":
                    away_yellow_cards += 1
                elif code == "HR":
                    home_red_cards += 1
                elif code == "AR":
                    away_red_cards += 1
                elif code == "HP":
                    home_penalty += 1
                elif code == "AP":
                    away_penalty += 1
                elif code == "HM":
                    home_penalty_missed += 1
                elif code == "AM":
                    away_penalty_missed += 1
                elif code == "HD":
                    home_goal_denied += 1
                elif code == "AD":
                    away_goal_denied += 1
                elif code == "HW":
                    home_substitute += 1
                elif code == "AW":
                    away_substitute += 1
                elif code == "HO":
                    home_own_goal += 1
                elif code == "AO":
                    away_own_goal += 1

                elif code == "RHY":
                    home_yellow_card -= 1
                elif code == "RAY":
                    away_yellow_cards -= 1
                elif code == "RHR":
                    home_red_cards -= 1
                elif code == "RAR":
                    away_red_cards -= 1
                elif code == "RHP":
                    home_penalty -= 1
                elif code == "RAP":
                    away_penalty -= 1
                elif code == "RHM":
                    home_penalty_missed -= 1
                elif code == "RAM":
                    away_penalty_missed -= 1
                elif code == "RHD":
                    home_goal_denied -= 1
                elif code == "RAD":
                    away_goal_denied -= 1
                elif code == "RHW":
                    home_substitute -= 1
                elif code == "RAW":
                    away_substitute -= 1
                elif code == "RHO":
                    home_own_goal -= 1
                elif code == "RAO":
                    away_own_goal -= 1
                else:
                    if not first_half_over:
                        first_half_extra = code
                        first_half_over = True
                        print("first_half_extra", first_half_extra)
                    else:
                        second_half_extra = code
                        print("second_half_extra", second_half_extra)

            write(home_yellow_card, file)  # home_yellow_card
            write(away_yellow_cards, file)  # away_yellow_cards
            write(home_red_cards, file)  # home_red_cards
            write(away_red_cards, file)  # away_red_cards
            write(home_penalty, file)  # home_penalty
            write(away_penalty, file)  # away_penalty
            write(home_penalty_missed, file)  # home_penalty_missed
            write(away_penalty_missed, file)  # away_penalty_missed
            write(home_goal_denied, file)  # home_goal_denied
            write(away_goal_denied, file)  # away_goal_denied
            write(home_substitute, file)  # home_substitute
            write(away_substitute, file)  # away_substitute
            write(home_own_goal, file)  # home_own_goal
            write(away_own_goal, file)  # away_own_goal
            write(first_half_extra, file)  # first_half_extra
            writeLast(second_half_extra, file)  # second_half_extra


def ask(text, file):
    data = input(text)
    file.write(str(data) + ", ")


def askLast(text, file):
    data = input(text)
    file.write(str(data) + "\n")


def write(text, file):
    file.write(str(text) + ", ")


def writeLast(text, file):
    file.write(str(text) + "\n")


askUser()
