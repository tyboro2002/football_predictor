from models.team import Team
from models.game import FootballGame


def parse_match_list(save_location):
    with open(save_location, "r", encoding="utf-8") as file:
        teams = [Team(team_name.strip()) for team_name in file.readline().split(",")]
        titles = [word.strip() for word in file.readline().split(",")]
        lines = [line.strip() for line in file.readlines()]
        matches = []
        for line in lines:
            if not line.startswith("#") and line.strip():
                line = line.split(",")
                match_data = {titles[i]: line[i].strip() for i in range(len(titles))}
                print(match_data)
                home_team = teams[int(match_data['home_team'])]
                away_team = teams[int(match_data['away_team'])]
                match = FootballGame(home_team, away_team)
                for key, value in match_data.items():
                    if key not in ['home_team', 'away_team']:
                        setattr(match, key, value)
                matches.append(match)

        return matches
