import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from parser import create_df_from_matchList


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
    return ''.join(form)  # Get the last 5 matches.csv form


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
    plt.close(fig)


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
    plt.close(fig)


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


def sort_and_divide_df(df, metric):
    # Sort the DataFrame by total_goals_scored
    agg_df_sorted = df.sort_values(by=metric, ascending=False)

    # Select only the 'team' and 'total_goals_scored' columns
    agg_df_sorted = agg_df_sorted[['team', metric]]
    return agg_df_sorted


def sort_teams_on_metrics(match_data, get_metric_sort_location):
    df = create_df_from_matchList(match_data)
    agg_df = df.groupby('team').agg({
        'goals_scored': "sum",
        'goals_conceded': "sum",
        'possession': "mean",
        'possession_conceded': "mean",
        'shots_on_target': "sum",
        'shots_on_target_conceded': "sum",
        'shots_wide_of_target': "sum",
        'shots_wide_of_target_conceded': "sum",
        'corners': "sum",
        'corners_conceded': "sum",
        'free_kicks': "sum",
        'free_kicks_conceded': "sum",
        'offside': "sum",
        'offside_conceded': "sum",
        'fouls': "sum",
        'fouls_conceded': "sum",
        'yellow_cards': "sum",
        'yellow_cards_opponent': "sum",
        'red_cards': "sum",
        'red_cards_opponent': "sum",
        'penalty': "sum",
        'penalty_conceded': "sum",
        'penalty_missed': "sum",
        'penalty_stopped': "sum",
        'goal_denied': "sum",
        'goal_denied_opponent': "sum",
        'substitute': "sum",
        'substitute_opponent': "sum",
        'own_goal_opponent': "sum",
        'own_goal_self': "sum",
        'first_half_extra': ['mean', 'sum'],
        'second_half_extra': ['mean', 'sum'],
        'play_time': ['mean', 'sum']
    }).reset_index()
    agg_df.columns = [
        'team',
        'total_goals_scored',
        'total_goals_conceded',
        'mean_possession',
        'mean_possession_conceded',
        'total_shots_on_target',
        'total_shots_on_target_conceded',
        'total_shots_wide_of_target',
        'total_shots_wide_of_target_conceded',
        'total_corners',
        'total_corners_conceded',
        'total_free_kicks',
        'total_free_kicks_conceded',
        'total_offside',
        'total_offside_conceded',
        'total_fouls',
        'total_fouls_conceded',
        'total_yellow_cards',
        'total_yellow_cards_opponent',
        'total_red_cards',
        'total_red_cards_opponent',
        'total_penalty',
        'total_penalty_conceded',
        'total_penalty_missed',
        'total_penalty_stopped',
        'total_goal_denied',
        'total_goal_denied_opponent',
        'total_substitute',
        'total_substitute_opponent',
        'total_own_goal_opponent',
        'total_own_goal_self',
        'mean_first_half_extra',
        'total_first_half_extra',
        'mean_second_half_extra',
        'total_second_half_extra',
        'mean_play_time',
        'total_play_time',
    ]

    # print(agg_df)
    # print(agg_df.columns.to_list())
    for metric in ['total_goals_scored', 'total_goals_conceded', 'mean_possession', 'mean_possession_conceded',
                   'total_shots_on_target', 'total_shots_on_target_conceded', 'total_shots_wide_of_target',
                   'total_shots_wide_of_target_conceded', 'total_corners', 'total_corners_conceded', 'total_free_kicks',
                   'total_free_kicks_conceded', 'total_offside', 'total_offside_conceded', 'total_fouls',
                   'total_fouls_conceded', 'total_yellow_cards', 'total_yellow_cards_opponent', 'total_red_cards',
                   'total_red_cards_opponent', 'total_penalty', 'total_penalty_conceded', 'total_penalty_missed',
                   'total_penalty_stopped', 'total_goal_denied', 'total_goal_denied_opponent', 'total_substitute',
                   'total_substitute_opponent', 'total_own_goal_opponent', 'total_own_goal_self',
                   'mean_first_half_extra', 'total_first_half_extra', 'mean_second_half_extra',
                   'total_second_half_extra', 'mean_play_time', 'total_play_time']:
        with open(get_metric_sort_location(metric), 'w') as file:
            result_df = sort_and_divide_df(agg_df, metric)

            # Write the DataFrame to a CSV file
            result_df.to_csv(file, index=False, lineterminator="\n")
