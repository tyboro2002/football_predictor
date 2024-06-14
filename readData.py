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
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            input_path = os.path.join(directory, filename)
            output_path = os.path.join(directory, filename)
            normalize_csv_file(input_path, output_path)
            print(f"Normalized {filename} and saved as {filename}")


def read_and_combine_csv(directory):
    dataframes = []

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            try:
                df = pd.read_csv(file_path, header=0)
                dataframes.append(df)
            except pd.errors.ParserError as e:
                print(f"Error reading {file_path}: {e}")
            except Exception as e:
                print(f"Unexpected error with {file_path}: {e}")

    if not dataframes:
        return pd.DataFrame()  # Return an empty DataFrame if no valid files were read

    combined_df = pd.concat(dataframes, ignore_index=True).fillna('')
    return combined_df


# Directory containing the CSV files
directory_path = "input_data/footbal-data-co-uk/Belgium/"

# Normalize all CSV files in the directory
normalize_all_csv_files_in_directory(directory_path)

# Read and combine all CSV files into a single DataFrame
combined_dataframe = read_and_combine_csv(directory_path)

# Display the first few rows of the combined DataFrame
print(combined_dataframe.head())
print(combined_dataframe.columns)

# Optionally, save the combined DataFrame to a new CSV file
# combined_dataframe.to_csv("combined_data.csv", index=False)
