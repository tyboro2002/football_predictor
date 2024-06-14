import pandas as pd
import os
import csv


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


def read_and_combine_csv(directory, column_merges={}, selected_columns=[], NaN_Value=0):
    dataframes = []

    # Iterate through all files and subdirectories in the directory
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".csv"):
                file_path = os.path.join(directory, filename)
                try:
                    df = pd.read_csv(file_path, header=0)
                    # df['source_file'] = file_path  # Add a column with the file path
                    df.fillna(NaN_Value, inplace=True)
                    dataframes.append(df)
                except pd.errors.ParserError as e:
                    print(f"Error reading {file_path}: {e}")
                except Exception as e:
                    print(f"Unexpected error with {file_path}: {e}")

    if not dataframes:
        return pd.DataFrame()  # Return an empty DataFrame if no valid files were read

    combined_df = pd.concat(dataframes, ignore_index=True).fillna('')

    # Select specific columns if they exist in the DataFrame
    selected_columns = [col for col in selected_columns if col in combined_df.columns]
    combined_dataframe = combined_df[selected_columns]

    # Merge specified columns
    for new_column, cols_to_merge in column_merges.items():
        combined_dataframe = combine_columns(combined_dataframe, cols_to_merge, new_column)

    return combined_dataframe


def combine_columns(df, column_list, new_column_name):
    if len(column_list) < 2:
        raise ValueError("column_list must contain at least two columns.")

    # Check if columns exist in the DataFrame
    existing_columns = [col for col in column_list if col in df.columns]
    if not len(existing_columns) == len(column_list):
        return df
    # Create a new column with the combined data
    df[new_column_name] = df[column_list[0]].combine_first(df[column_list[1]])  # TODO this now gives a warning fix

    # Drop the original columns
    df.drop(columns=existing_columns, inplace=True)
    return df


# Define the columns you want to select
selected_columns = [
    'HomeTeam', 'AwayTeam',
    'FTHG', 'FTAG',  # it's this row or
    # 'HG', 'AG'  # this row
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
    # 'Res'
    # 'source_file'
]

column_merges = {
    # 'FTR': ['FTR', 'Res'],
    # 'FTHG': ['FTHG', 'HG'],
    # 'FTAG': ['FTAG', 'AG'],
}

# Directory containing the CSV files
directory_path = "input_data/footbal-data-co-uk/"

# Normalize all CSV files in the directory
normalize_all_csv_files_in_directory(directory_path)

# Read and combine all CSV files into a single DataFrame
combined_dataframe = read_and_combine_csv(directory_path, column_merges=column_merges, selected_columns=selected_columns)

# pd.set_option('display.max_columns', None)   # Display all columns
# pd.set_option('display.max_rows', None)      # Display all rows in each cell
# pd.set_option('display.max_colwidth', None)  # Do not truncate column content
# pd.set_option('display.width', None)         # Do not wrap around output

# Display the first few rows of the combined DataFrame
print(combined_dataframe)
print(combined_dataframe.columns)

# Optionally, save the combined DataFrame to a new CSV file
# combined_dataframe.to_csv("combined_data.csv", index=False)
