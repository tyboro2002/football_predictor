from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from parser import parse_match_list
from settings import match_list_location
import pandas as pd

estimators = 100_000

match_data = parse_match_list(match_list_location)
print(len(match_data))
df = pd.DataFrame([data.__dict__ for data in match_data])

# Convert team columns to string representations
df['home'] = df['home'].apply(str)
df['away'] = df['away'].apply(str)

codes = {"Dender":0, "Union":1, "Anderlecht":2, "Antwerpen":3, "Club brugge":4, "Cercle brugge":5, "Krc genk":6, "Gent":7, "Kv mechelen":8, "Stvv":9, "Standard":10, "Westerlo":11 ,"Oh leuven":12, "Charleroi":13, "Kas eupen":14, "Kv korterijk":15, "Rwdm":16}

# Replace numerical team values with their string representations
df['home'] = df['home'].map(codes)
df['away'] = df['away'].map(codes)


# Assuming you have a DataFrame called 'data' containing your features and target variable
X = df.drop(['home_score', 'away_score'], axis=1)
y_home = df['home_score']
y_away = df['away_score']


# Split the data into training and testing sets
X_train, X_test, y_train_home, y_test_home, y_train_away, y_test_away = train_test_split(X, y_home, y_away)

# Train separate models for home and away scores
model_home = RandomForestRegressor(n_estimators=estimators)
model_home.fit(X_train, y_train_home)

model_away = RandomForestRegressor(n_estimators=estimators)
model_away.fit(X_train, y_train_away)

# Evaluate the models
y_pred_home = model_home.predict(X_test)
y_pred_away = model_away.predict(X_test)

mse_home = mean_squared_error(y_test_home, y_pred_home)
mse_away = mean_squared_error(y_test_away, y_pred_away)

print(f"Mean Squared Error (Home Score): {mse_home}")
print(f"Mean Squared Error (Away Score): {mse_away}")
print("\n\n")

# Make predictions
new_data = pd.read_csv("input_data/toPredict.csv")  # Your new data for prediction
new_data.columns = new_data.columns.map(lambda x: x.strip() if isinstance(x, str) else x)
new_data['home'] = new_data['home'].apply(str)
new_data['away'] = new_data['away'].apply(str)
new_data['home'] = new_data['home'].map(codes)
new_data['away'] = new_data['away'].map(codes)
X = new_data.drop(['home_score', 'away_score'], axis=1)
y_home = new_data['home_score']
y_away = new_data['away_score']

home_score_prediction = model_home.predict(X)
away_score_prediction = model_away.predict(X)

correct_ones = 0
GD_correct = 0
winner_correct = 0

for i in range(len(home_score_prediction)):
    home_team_name = new_data.loc[i, 'home']
    away_team_name = new_data.loc[i, 'away']

    print(f"Predicted Home Score for data point {i} ({home_team_name}): {home_score_prediction[i]} (Rounded down: {int(home_score_prediction[i])})")
    print(f"Predicted Away Score for data point {i} ({away_team_name}): {away_score_prediction[i]} (Rounded down: {int(away_score_prediction[i])})")

    actual_home_score = y_home[i]
    actual_away_score = y_away[i]

    print(f"Actual Home Score for data point {i}: {actual_home_score}")
    print(f"Actual Away Score for data point {i}: {actual_away_score}")

    # Check if predicted scores match actual scores
    if int(home_score_prediction[i]) == actual_home_score:
        print("Predicted Home Score matches actual Home Score!")
    else:
        print("Predicted Home Score does not match actual Home Score!")

    if int(away_score_prediction[i]) == actual_away_score:
        print("Predicted Away Score matches actual Away Score!")
    else:
        print("Predicted Away Score does not match actual Away Score!")

    if (int(home_score_prediction[i]) - int(away_score_prediction[i])) == (actual_home_score - actual_away_score):
        print("Predicted GD matches actual GD!")
        GD_correct += 1
    else:
        print("Predicted GD does not match actual GD!")

    if int(home_score_prediction[i]) == actual_home_score and int(away_score_prediction[i]) == actual_away_score:
        print("Predicted exact correct!")
        correct_ones += 1

    if int(home_score_prediction[i]) < int(away_score_prediction[i]) and actual_home_score < actual_away_score or int(home_score_prediction[i]) > int(away_score_prediction[i]) and actual_home_score > actual_away_score or int(home_score_prediction[i]) == int(away_score_prediction[i]) and actual_home_score == actual_away_score:
        print("Predicted winner correct!")
        winner_correct += 1
    print("\n")

amount_of_matches = len(y_home)
print("matches", amount_of_matches)
print("winner_correct", winner_correct)
print("GD correct", GD_correct)
print("exact correct", correct_ones)

percentage_winner_correct = (winner_correct / amount_of_matches) * 100
percentage_GD_correct = (GD_correct / amount_of_matches) * 100
percentage_exact_correct = (correct_ones / amount_of_matches) * 100

print("Percentage of winner predictions correct:", percentage_winner_correct)
print("Percentage of GD predictions correct:", percentage_GD_correct)
print("Percentage of exact predictions correct:", percentage_exact_correct)
