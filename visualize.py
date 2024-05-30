import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def visualize_position_chances(data, save_location, League):
    # Convert the data to a DataFrame
    df = pd.DataFrame(data, index=[f'Position {i + 1}' for i in range(len(League.teams))])

    # Create a heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.T, annot=True, cmap='coolwarm', fmt=".3f", linewidths=.5)
    plt.title("Probability of Teams Finishing in Each Position")
    plt.xlabel("Position")
    plt.ylabel("Team")

    # Save the figure
    plt.savefig(save_location)


def calculate_team_form(team, last_matchdays_results):
    # Simulate form calculation based on match results
    form = []
    for matchday in last_matchdays_results:
        for match in matchday:
            if match.home.name == team:
                if match.home_score > match.away_score:
                    form.append('W')
                elif match.home_score < match.away_score:
                    form.append('L')
                else:
                    form.append('D')
            elif match.away.name == team:
                if match.home_score > match.away_score:
                    form.append('L')
                elif match.home_score < match.away_score:
                    form.append('W')
                else:
                    form.append('D')

    # Combine the form into a string
    return ''.join(form)  # Get the last 5 matches form


def visualize_league(league, save_location):
    last_matchdays_results = league.matchdays[-5:]
    # Transform the data into a DataFrame
    data = []
    for team, stats in league.get_standings():
        diff = stats['scored'] - stats['conceded']
        row = [team, stats['points'], stats['played'], stats['won'], stats['drawn'], stats['lost'], stats['scored'],
               stats['conceded'], diff]

        form = calculate_team_form(team, last_matchdays_results)
        row.append(form)

        data.append(row)

    columns = ['TEAM', 'Pts', 'PG', 'W', 'D', 'L', 'GF', 'GA', 'DIFF', 'FORM']
    df = pd.DataFrame(data, columns=columns)

    # Create the table using matplotlib
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('tight')
    ax.axis('off')

    # Add a table
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.3, 1.3)

    # Apply colors to headers
    header_color = '#d4a373'  # Yellow-brown color
    for key, cell in table.get_celld().items():
        row, col = key
        if row == 0:
            cell.set_fontsize(14)
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(header_color)
        else:
            if col == 1:  # Points column
                cell.set_fontsize(14)
                cell.set_text_props(weight='bold', color=header_color)
            else:
                cell.set_text_props(color='white')
            cell.set_facecolor('#404040' if row % 2 == 0 else '#606060')

    # Save the figure
    plt.savefig(save_location)


def visualize_match_list(data, save_location):
    columns = ['Home Team', 'Result', 'Away Team']
    df = pd.DataFrame(data, columns=columns)

    # Create the table using matplotlib
    fig, ax = plt.subplots(figsize=(8, len(data) * 0.6))
    ax.axis('tight')
    ax.axis('off')

    # Add a table
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.3, 1.3)

    # Apply colors to headers
    header_color = '#d4a373'  # Yellow-brown color
    for key, cell in table.get_celld().items():
        row, col = key
        if row == 0:
            cell.set_fontsize(14)
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(header_color)
        else:
            if col == 1:  # Result column
                cell.set_text_props(weight='bold')
            result = df.iloc[row - 1, 1]
            home_score, away_score = map(int, result.split('-'))
            if home_score > away_score and col == 0:
                cell.set_text_props(weight='bold')
            if home_score < away_score and col == 2:
                cell.set_text_props(weight='bold')
            cell.set_facecolor('#404040' if row % 2 == 0 else '#606060')

    # Save the figure
    plt.savefig(save_location, bbox_inches='tight')


def visualize_matchday_results(matchday_results, save_location):
    # Transform the data into a DataFrame
    data = []
    for match in matchday_results:
        home_team = match.home
        away_team = match.away
        home_score = match.home_score
        away_score = match.away_score
        result = f"{home_score}-{away_score}"
        data.append([home_team, result, away_team])
    visualize_match_list(data, save_location)


def visualize_league_matches(league, save_location):
    for i in range(len(league.matchdays)):
        visualize_matchday_results(league.matchdays[i], save_location(i + 1))


def visualize_team_matches(league, team_name, save_location):
    # Transform the data into a DataFrame
    data = []
    for matchday in league.matchdays:
        for match in matchday:
            if match.home.name == team_name or match.away.name == team_name:
                home_team = match.home
                away_team = match.away
                home_score = match.home_score
                away_score = match.away_score
                result = f"{home_score}-{away_score}"
                data.append([home_team, result, away_team])
    visualize_match_list(data, save_location)

def visualize_all_team_matches(league, save_location):
    team_names = [team.name for team in league.teams]
    for team in team_names:
        visualize_team_matches(league, team, save_location(team))
