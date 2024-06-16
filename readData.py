import pandas as pd
import os
import csv
import seaborn as sns
import matplotlib.pyplot as plt

from visualize import make_histogram

# Directory containing the CSV files
directory_path = "input_data/footbal-data-co-uk"
output_path = "input_data/merged/merged.csv"

insert_columns = [
    ('ball_possession_home_team', 7, 0),
    ('home_shots_wide_of_target', 12, 0),
    ('away_shots_wide_of_target', 13, 0),
    ('home_penalty', 31, 0),
    ('away_penalty', 32, 0),
    ('home_penalty_missed', 33, 0),
    ('away_penalty_missed', 34, 0),
    ('home_goal_denied', 35, 0),
    ('away_goal_denied', 36, 0),
    ('home_substitute', 37, 0),
    ('away_substitute', 38, 0),
    ('home_own_goal', 39, 0),
    ('away_own_goal', 40, 0),
    ('first_half_extra_time', 41, 0),
    ('second_half_extra_time', 42, 0),
]

new_colum_names = [
    'Div', 'Date', 'Time',
    'home_team', 'away_team',
    'home_score', 'away_score',
    'ball_possession_home_team',
    'home_shots', 'away_shots',
    'home_shots_on_target', 'away_shots_on_target',
    'home_shots_wide_of_target', 'away_shots_wide_of_target',
    'home_shots_hit_woodwork', 'away_shots_hit_woodwork',
    'home_corners', 'away_corners',
    'home_fouls', 'away_fouls',
    'home_free_kicks', 'away_free_kicks',
    'home_offside', 'away_offside',
    'home_yellow_card', 'away_yellow_card',
    'home_red_cards', 'away_red_cards',
    'home_team_bookings_points', 'away_team_bookings_points',
    'final_time_result',
    'home_penalty', 'away_penalty',
    'home_penalty_missed', 'away_penalty_missed',
    'home_goal_denied', 'away_goal_denied',
    'home_substitute', 'away_substitute',
    'home_own_goal', 'away_own_goal',
    'first_half_extra_time', 'second_half_extra_time',
    'source_file',
]

# Define the columns you want to select
selected_columns = [
    'Div', 'Date', 'Time',
    'HomeTeam', 'AwayTeam',
    'FTHG', 'FTAG',  # it's this row or
    'HG', 'AG',  # this row
    'HS', 'AS',
    'HST', 'AST',
    'HHW', 'AHW',
    'HC', 'AC',
    'HF', 'AF',
    'HFKC', 'AFKC',
    'HO', 'AO',
    'HY', 'AY',
    'HR', 'AR',
    'HBP', 'ABP',
    'FTR',  # both are the same
    'Res',
    'source_file'
]

column_merges = {
    'FTR': ['FTR', 'Res'],
    'FTHG': ['FTHG', 'HG'],
    'FTAG': ['FTAG', 'AG'],
}


def normalize_csv_file(input_file, output_file):
    # Read the CSV file to find the maximum number of fields in any row
    max_fields = 0
    rows = []
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            max_fields = max(max_fields, len(row))
            rows.append(row)

    # Pad rows with missing fields with empty values
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            if len(row) < max_fields:
                row.extend([''] * (max_fields - len(row)))
            writer.writerow(row)


def normalize_all_csv_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".csv"):
                input_path = os.path.join(root, filename)
                output_path = os.path.join(root, filename)
                normalize_csv_file(input_path, output_path)
                print(f"Normalized {filename} and saved as {filename}")


def read_and_combine_csv(directory, column_merges={}, selected_columns=[], NaN_Value=0, encoding='utf-8'):
    dataframes = []

    # Iterate through all files and subdirectories in the directory
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".csv"):
                file_path = os.path.join(root, filename)
                try:
                    df = pd.read_csv(file_path, header=0, encoding=encoding)
                    df['source_file'] = file_path  # Add a column with the file path
                    df.fillna(NaN_Value, inplace=True)
                    dataframes.append(df)
                except pd.errors.ParserError as e:
                    print(f"Error reading {file_path}: {e}")
                except Exception as e:
                    print(f"Unexpected error with {file_path}: {e}")

    if not dataframes:
        return pd.DataFrame()  # Return an empty DataFrame if no valid files were read

    combined_df = pd.concat(dataframes, ignore_index=True).fillna('')

    # Replace all empty strings with NaN_Value (which is 0 in this case)
    combined_df.replace('', NaN_Value, inplace=True)

    # Select specific columns if they exist in the DataFrame
    selected_columns = [col for col in selected_columns if col in combined_df.columns]
    combined_dataframe = combined_df[selected_columns]

    # Merge specified columns
    for new_column, cols_to_merge in column_merges.items():
        combined_dataframe = combine_columns(combined_dataframe, cols_to_merge, new_column)

    # Keep only rows where 'home_team' and 'away_team' exist
    if 'HomeTeam' in combined_dataframe.columns and 'AwayTeam' in combined_dataframe.columns:
        combined_dataframe = combined_dataframe[
            (combined_dataframe['HomeTeam'] != '') & (combined_dataframe['AwayTeam'] != '') &
            (combined_dataframe['HomeTeam'] != 0) & (combined_dataframe['AwayTeam'] != 0)
            ]

    # Replace all empty strings with NaN_Value (which is 0 in this case)
    combined_df.replace('', NaN_Value, inplace=True)

    # Attempt to convert each column to integers where possible
    for column in combined_dataframe.columns:
        # Check if the column can be converted to numeric without changing its data type to avoid converting text
        combined_dataframe[column] = pd.to_numeric(combined_dataframe[column], errors='ignore')
        try:
            combined_dataframe[column] = combined_dataframe[column].astype(int)
        except ValueError:
            pass

    return combined_dataframe


def combine_columns(df, column_list, new_column):
    # Ensure all columns in column_list exist in the DataFrame
    existing_columns = [col for col in column_list if col in df.columns]

    if existing_columns:
        # Mask the rows of the second column where there is a value in the first column
        if len(existing_columns) > 1:
            df.loc[df[existing_columns[0]] != '', existing_columns[1]] = ''

        # Create the new column by concatenating values from the existing columns
        df[new_column] = df[existing_columns].astype(str).agg(''.join, axis=1)

    existing_columns.remove(new_column)
    # Drop the original columns
    df.drop(columns=existing_columns, inplace=True)

    return df


# Normalize all CSV files in the directory
# normalize_all_csv_files_in_directory(directory_path)

# Read and combine all CSV files into a single DataFrame
combined_dataframe = read_and_combine_csv(
    directory_path,
    column_merges=column_merges,
    selected_columns=selected_columns
)

# Insert new columns with all zeros at specific positions
for col_name, pos, value in insert_columns:
    combined_dataframe.insert(pos, col_name, value)

combined_dataframe.columns = new_colum_names

# pd.set_option('display.max_columns', None)   # Display all columns
# pd.set_option('display.max_rows', None)      # Display all rows in each cell
# pd.set_option('display.max_colwidth', None)  # Do not truncate column content
# pd.set_option('display.width', None)         # Do not wrap around output

# Display the first few rows of the combined DataFrame
print(combined_dataframe)
# print(combined_dataframe.columns)

# # Get and print the types of the values in the FTR column
# if 'FTHG' in combined_dataframe.columns:
#     ftr_types = combined_dataframe['FTHG'].apply(type)
#     print(ftr_types)
# else:
#     print("The 'FTHG' column does not exist in the DataFrame.")

# Optionally, save the combined DataFrame to a new CSV file
combined_dataframe.to_csv(output_path, index=False)

# Read the CSV file into a DataFrame
df = pd.read_csv(output_path)

# Count the number of rows in the DataFrame
num_lines = df.shape[0]
print(df.columns)

# Print the number of lines
print(f"Number of lines in '{output_path}': {num_lines}")


# Function to extract year from date
def extract_year(date_str):
    year = int(date_str[-2:])
    if year <= 50:  # Assuming 00-50 are from 2000s
        return 2000 + year
    else:
        return 1900 + year


# Function to filter matches within a specific year range
def filter_matches_by_year(df, start_year, end_year):
    filtered_df = df
    filtered_df['Year'] = filtered_df['Date'].apply(extract_year)
    filtered_df = filtered_df[(filtered_df['Year'] >= start_year) & (filtered_df['Year'] <= end_year)]
    filtered_df.drop(columns=['Year'], inplace=True)
    return filtered_df


# Filter matches between 2018 and 2020
filtered_df = filter_matches_by_year(df, 1920, 2000)

make_histogram(df['final_time_result'], 'final_time_result')
make_histogram(abs(df['home_score'] - df['away_score']), 'goal differences')
make_histogram(df['home_score'] - df['away_score'], 'home score - away score')
make_histogram(filtered_df['final_time_result'], 'final_time_result')
