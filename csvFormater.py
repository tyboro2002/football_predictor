inp_file = "input_data/inp.csv"


def askUser():
    # Writing to file
    with open(inp_file, "w") as file:
        write("home_team, away_team, home_score, away_score, ball_possession_home_team, home_shots_on_target, away_shots_on_target, home_shots_wide_of_target, away_shots_wide_of_target, home_corners, away_corners, home_free_kicks, away_free_kicks, home_offside, away_offside, home_fouls, away_fouls, home_yellow_cards, away_yellow_cards, home_red_cards, away_red_cards, home_penalty, away_penalty, home_penalty_missed, away_penalty_missed, home_goal_denied, away_goal_denied, home_substitute, away_substitute, home_own_goal, away_own_goal, first_half_extra_time, second_half_extra_time", file, end="\n")
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

            home_yellow_cards = 0
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
                try:
                    num_retract = int(''.join(filter(str.isdigit, code)))
                except ValueError:
                    num_retract = 1
                if "END" in code:
                    break

                elif "RHY" in code and home_yellow_cards >= num_retract:
                    home_yellow_cards -= num_retract
                elif "RAY" in code and away_yellow_cards >= num_retract:
                    away_yellow_cards -= num_retract
                elif "RHR" in code and home_red_cards >= num_retract:
                    home_red_cards -= num_retract
                elif "RAR" in code and away_red_cards >= num_retract:
                    away_red_cards -= num_retract
                elif "RHP" in code and home_penalty >= num_retract:
                    home_penalty -= num_retract
                elif "RAP" in code and away_penalty >= num_retract:
                    away_penalty -= num_retract
                elif "RHM" in code and home_penalty_missed >= num_retract:
                    home_penalty_missed -= num_retract
                elif "RAM" in code and away_penalty_missed >= num_retract:
                    away_penalty_missed -= num_retract
                elif "RHD" in code and home_goal_denied >= num_retract:
                    home_goal_denied -= num_retract
                elif "RAD" in code and away_goal_denied >= num_retract:
                    away_goal_denied -= num_retract
                elif "RHW" in code and home_substitute >= num_retract:
                    home_substitute -= num_retract
                elif "RAW" in code and away_substitute >= num_retract:
                    away_substitute -= num_retract
                elif "RHO" in code and home_own_goal >= num_retract:
                    home_own_goal -= num_retract
                elif "RAO" in code and away_own_goal >= num_retract:
                    away_own_goal -= num_retract
                elif "RFH" in code and first_half_over:
                    first_half_over = False
                    second_half_extra = 0

                elif "HY" in code and "R" not in code:
                    home_yellow_cards += num_retract
                elif "AY" in code and "R" not in code:
                    away_yellow_cards += num_retract
                elif "HR" in code and "RHR" not in code:
                    home_red_cards += num_retract
                elif "AR" in code and "RAR" not in code:
                    away_red_cards += num_retract
                elif "HP" in code and "R" not in code:
                    home_penalty += num_retract
                elif "AP" in code and "R" not in code:
                    away_penalty += num_retract
                elif "HM" in code and "R" not in code:
                    home_penalty_missed += num_retract
                elif "AM" in code and "R" not in code:
                    away_penalty_missed += num_retract
                elif "HD" in code and "R" not in code:
                    home_goal_denied += num_retract
                elif "AD" in code and "R" not in code:
                    away_goal_denied += num_retract
                elif "HW" in code and "R" not in code:
                    home_substitute += num_retract
                elif "AW" in code and "R" not in code:
                    away_substitute += num_retract
                elif "HO" in code and "R" not in code:
                    home_own_goal += num_retract
                elif "AO" in code and "R" not in code:
                    away_own_goal += num_retract
                else:
                    try:
                        if not first_half_over:
                            first_half_extra = int(code)
                            first_half_over = True
                            print("first_half_extra", first_half_extra)
                        else:
                            second_half_extra = int(code)
                            print("second_half_extra", second_half_extra)
                    except ValueError:
                        print(f"Invalid: {code}")

            write(home_yellow_cards, file)  # home_yellow_cards
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
            write(second_half_extra, file, end="\n")  # second_half_extra


def ask(text, file, end=", "):
    while True:
        try:
            data = int(input(text))
            if data < 0:
                raise ValueError("Input must be a positive integer.")
            file.write(str(data) + end)
            break  # Break the loop if input is valid
        except ValueError as e:
            print(e)  # Print error message
            continue  # Continue the loop to prompt for input again


def write(text, file, end=", "):
    file.write(str(text) + end)


askUser()
