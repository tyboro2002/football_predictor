import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from parser import create_df_from_matchList
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image, ImageDraw, ImageFont
from PIL import Image
import numpy as np

from models.game import FootballGame
from models.team import Team
from typing import List

# Paths to the logos
logos_path = "assets/logos/"

# Dictionary to cache images
image_cache = {}


# Function to create a placeholder image
def create_placeholder(text, size=(700, 700)):
    img = Image.new('RGB', size, color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    fnt = ImageFont.load_default()
    text_bbox = d.textbbox((0, 0), text, font=fnt)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    d.text(position, text, fill=(0, 0, 0), font=fnt)
    return img


# Function to load, resize, and process image with caching
def get_image(team_name: str, zoom=0.1, size=(700, 700)):
    path = logos_path + team_name.replace(" ", "_").capitalize() + ".png"
    if (team_name, size) in image_cache:
        image = image_cache[(team_name, size)]
    else:
        try:
            image = Image.open(path)
            image = image.resize(size)
        except FileNotFoundError:
            image = create_placeholder("N/A", size=size)
        image_cache[(team_name, size)] = image
    return OffsetImage(image, zoom=zoom)


def visualize_position_chances(data, save_location, league):
    # Convert the data to a DataFrame
    df = pd.DataFrame(data, index=[f'Position {i + 1}' for i in range(len(league.teams))])

    # Create a heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.T, annot=True, cmap='coolwarm', fmt=".3f", linewidths=.5)
    plt.title("Probability of Teams Finishing in Each Position")
    plt.xlabel("Position")
    plt.ylabel("Team")

    # Save the figure
    plt.savefig(save_location)


def visualize_group_standings_chanches(data, get_group_location, group_stage):
    for i in range(len(data)):
        group_data = data[i]
        visualize_position_chances(group_data, get_group_location(i), group_stage.leagues[i])


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
        create_match_day_visual(league.matchdays[i], i + 1, save_location(i + 1))
        # visualize_matchday_results(league.matchdays[i], save_location(i + 1))


def visualize_team_matches(league, team_name, save_location):
    # Transform the data into a DataFrame
    data = []
    for matchday in league.matchdays:
        for match in matchday:
            if match.home.name == team_name or match.away.name == team_name:
                data.append(match)
    create_match_list_visual(data, team_name, save_location)

    # visualize_match_list(data, save_location)


def visualize_all_team_matches(league, save_location):
    team_names = [team.name for team in league.teams]
    for team in team_names:
        visualize_team_matches(league, team, save_location(team))


def sort_and_divide_df(df, metric, additional_columns=[]):
    """
    Sort the DataFrame by a specified metric and keep additional columns if provided.

    Parameters:
    - df: The DataFrame to sort.
    - metric: The column name to sort by.
    - additional_columns: List of additional columns to include in the resulting DataFrame. Default is an empty list.

    Returns:
    - A sorted DataFrame containing the specified metric and additional columns.
    """
    # Ensure additional_columns is a list
    if not isinstance(additional_columns, list):
        raise ValueError("additional_columns should be a list")

    # Determine the columns to keep
    columns_to_keep = ['team', metric] + additional_columns

    # Sort the DataFrame by the specified metric
    agg_df_sorted = df.sort_values(by=metric, ascending=False)

    # Select the specified columns
    agg_df_sorted = agg_df_sorted[columns_to_keep]

    return agg_df_sorted


def sort_teams_on_metrics(df, get_metric_sort_location):
    agg_df = df.groupby('team').agg({
        'goals_scored': "sum",
        'goals_conceded': "sum",
        'goals_difference': ['mean', 'sum'],
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
        'mean_goals_difference',
        'total_goals_difference',
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

    for metric in ['total_goals_scored', 'total_goals_conceded', 'mean_goals_difference', 'total_goals_difference',
                   'mean_possession', 'mean_possession_conceded', 'total_shots_on_target',
                   'total_shots_on_target_conceded', 'total_shots_wide_of_target',
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


# Function to create match list visual
def create_match_list_visual(matches: List[FootballGame], title, save_location, fontSizeName=14, fontSizeScore=20,
                             fontSizeTitle=24):
    # Create a figure
    fig, ax = plt.subplots(figsize=(10, 14))

    # Set the background color
    fig.patch.set_facecolor('black')

    # Hide the axes
    ax.axis('off')

    size = (200, 200)

    # Iterate through matches to add logos and text
    for i, match in enumerate(matches):
        home: Team = match.home
        away: Team = match.away
        home_score = match.home_score
        away_score = match.away_score
        y = 1 - (i * 1 / (len(matches) + 1)) - 0.05  # Adjust vertical spacing

        # Home team
        home_logo = get_image(home.name, size=size)
        ab = AnnotationBbox(home_logo, (0.3, y), frameon=False)
        ax.add_artist(ab)
        ax.text(0.05, y, home.name, color='white', fontsize=fontSizeName, verticalalignment='center')

        # Away team
        away_logo = get_image(away.name, size=size)
        ab = AnnotationBbox(away_logo, (0.7, y), frameon=False)
        ax.add_artist(ab)
        ax.text(0.85, y, away.name, color='white', fontsize=fontSizeName, verticalalignment='center')

        ax.text(0.45, y, home_score, color='white', fontsize=fontSizeScore, verticalalignment='center')
        ax.text(0.50, y, "-", color='white', fontsize=fontSizeScore, verticalalignment='center')
        ax.text(0.55, y, away_score, color='white', fontsize=fontSizeScore, verticalalignment='center')

    # Title
    ax.text(0.5, 1.05, title, color='yellow', fontsize=fontSizeTitle, ha='center', va='center')

    # Save the figure
    plt.savefig(save_location, bbox_inches='tight')
    plt.close(fig)


# Function to create match day visual
def create_match_day_visual(matches: List[FootballGame], matchday, save_location, fontSizeName=14, fontSizeScore=20,
                            fontSizeTitle=24):
    # Create a figure
    fig, ax = plt.subplots(figsize=(10, 14))

    # Set the background color
    fig.patch.set_facecolor('black')

    # Hide the axes
    ax.axis('off')

    # Iterate through matches to add logos and text
    for i, match in enumerate(matches):
        home: Team = match.home
        away: Team = match.away
        home_score = match.home_score
        away_score = match.away_score
        y = 1 - (i * 0.125) - 0.05  # Adjust vertical spacing

        # Home team
        home_logo = get_image(home.name)
        ab = AnnotationBbox(home_logo, (0.3, y), frameon=False)
        ax.add_artist(ab)
        ax.text(0.05, y, home.name, color='white', fontsize=fontSizeName, verticalalignment='center')

        # Away team
        away_logo = get_image(away.name)
        ab = AnnotationBbox(away_logo, (0.7, y), frameon=False)
        ax.add_artist(ab)
        ax.text(0.85, y, away.name, color='white', fontsize=fontSizeName, verticalalignment='center')

        ax.text(0.45, y, home_score, color='white', fontsize=fontSizeScore, verticalalignment='center')
        ax.text(0.50, y, "-", color='white', fontsize=fontSizeScore, verticalalignment='center')
        ax.text(0.55, y, away_score, color='white', fontsize=fontSizeScore, verticalalignment='center')

    # Title
    ax.text(0.5, 1.05, f'MATCH DAY {matchday}', color='yellow', fontsize=fontSizeTitle, ha='center', va='center')

    # Save the figure
    plt.savefig(save_location, bbox_inches='tight')
    plt.close(fig)


def make_histogram(data, title: str, save_location=None, figsize=(10, 6)):
    # Plot the distribution of the values in 'final_time_result'
    plt.figure(figsize=figsize)
    sns.histplot(data)
    plt.title(f'Distribution of Values in {title}')
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    if save_location is not None:
        # Save the figure
        plt.savefig(save_location, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
