import pandas as pd
import requests
from io import StringIO

# Correct URLs of the datasets
urls = {
    "English Premier League": "https://datahub.io/sports-data/english-premier-league",
    "Spanish La Liga": "https://datahub.io/sports-data/spanish-la-liga",
    "Italian Serie A": "https://datahub.io/sports-data/italian-serie-a",
    "German Bundesliga": "https://datahub.io/sports-data/german-bundesliga",
    "French Ligue 1": "https://datahub.io/sports-data/french-ligue-1"
}

# Dictionary to store dataframes
dataframes = {}

# Headers to request CSV format explicitly
headers = {
    'Accept': 'text/csv'
}

# Fetch and read each dataset
for league, url in urls.items():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        csv_data = response.content.decode('utf-8')
        dataframes[league] = pd.read_csv(StringIO(csv_data))
        print(f"Successfully fetched data for {league}")
    else:
        print(f"Failed to fetch data for {league}, Status Code: {response.status_code}")

# Example: Display the first few rows of each dataframe
for league, df in dataframes.items():
    print(f"\n{league}:\n")
    print(df.head())
