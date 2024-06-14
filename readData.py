import pandas as pd
import os


def read_and_combine_csv(directory):
    # List to hold DataFrames
    dataframes = []

    # Determine the union of all columns
    all_columns = set()
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            all_columns.update(df.columns)

    all_columns = list(all_columns)

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)

            # Add missing columns
            for col in all_columns:
                if col not in df.columns:
                    df[col] = ''

            # Ensure the same order of columns
            df = df[all_columns]

            dataframes.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)

    return combined_df


# Directory containing the CSV files
directory_path = "input_data/footbal-data-co-uk/Belgium/"

# Read and combine all CSV files into a single DataFrame
combined_dataframe = read_and_combine_csv(directory_path)

# Display the first few rows of the combined DataFrame
print(combined_dataframe.head())

# Optionally, save the combined DataFrame to a new CSV file
# combined_dataframe.to_csv("combined_data.csv", index=False)
