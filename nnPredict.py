from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from parser import parse_match_list
from settings import match_list_location
import pandas as pd
import numpy as np
import random
import joblib  # For saving and loading models
from settings import codes

retrain_model = True
max_amount_of_training_matches = 1_000

# Define a noise level
noise_level = 5  # Adjust this value as needed

estimators = 10_000

amount_of_non_noisy_predictions = 5
amount_of_noisy_predictions = 30

silent = True


# Function to calculate recent form
def calculate_recent_form(df, team_col, home_score_col, away_score_col, window=5):
    recent_form = {team: [] for team in codes.values()}
    form_scores = []

    for index, row in df.iterrows():
        team = row[team_col]
        home_score = row[home_score_col]
        away_score = row[away_score_col]

        if team_col == 'home':
            if home_score > away_score:
                recent_form[team].append(3)  # Win
            elif home_score == away_score:
                recent_form[team].append(1)  # Draw
            else:
                recent_form[team].append(0)  # Loss
        else:
            if home_score < away_score:
                recent_form[team].append(3)  # Win
            elif home_score == away_score:
                recent_form[team].append(1)  # Draw
            else:
                recent_form[team].append(0)  # Loss

        if len(recent_form[team]) > window:
            recent_form[team].pop(0)

        form_scores.append(np.mean(recent_form[team]))

    return form_scores


def add_new_colls(df, rename_teams=False):
    if 'away_shots_hit_woodwork' in df.columns:
        df = df.drop(['away_shots_hit_woodwork', 'away_team_bookings_points', 'home_shots_hit_woodwork', 'home_team_bookings_points'], axis=1)
    if rename_teams:
        # Convert team columns to string representations
        df['home'] = df['home'].apply(str)
        df['away'] = df['away'].apply(str)

        # Replace numerical team values with their string representations
        df['home'] = df['home'].map(codes)
        df['away'] = df['away'].map(codes)

    df['home_recent_form'] = calculate_recent_form(df, 'home', 'home_score', 'away_score')
    df['away_recent_form'] = calculate_recent_form(df, 'away', 'away_score', 'home_score')
    # df['home_avg_goals_scored'] = df.groupby('home')['home_score'].transform(
    #     lambda x: x.rolling(window=5, min_periods=1).mean())
    # df['away_avg_goals_scored'] = df.groupby('away')['away_score'].transform(
    #     lambda x: x.rolling(window=5, min_periods=1).mean())
    # df['home_avg_goals_conceded'] = df.groupby('home')['away_score'].transform(
    #     lambda x: x.rolling(window=5, min_periods=1).mean())
    # df['away_avg_goals_conceded'] = df.groupby('away')['home_score'].transform(
    #     lambda x: x.rolling(window=5, min_periods=1).mean())

    # Goal Difference
    df['goal_difference'] = (df.groupby('home')['home_score'].transform(
             lambda x: x.rolling(window=5, min_periods=1).mean()) -
                             df.groupby('home')['away_score'].transform(
             lambda x: x.rolling(window=5, min_periods=1).mean()))

    # Team Strength Difference
    # df['team_strength_difference'] = df['home_avg_goals_scored'] - df['away_avg_goals_scored']

    # Total Goals Scored and Conceded
    # df['total_goals_scored'] = df['home_avg_goals_scored'] + df['away_avg_goals_scored']
    # df['total_goals_conceded'] = df['home_avg_goals_conceded'] + df['away_avg_goals_conceded']

    # Home and Away Win Ratios
    df['home_win_ratio'] = df.groupby('home')['home_recent_form'].transform(lambda x: np.mean(x == 3))
    df['away_win_ratio'] = df.groupby('away')['away_recent_form'].transform(lambda x: np.mean(x == 3))

    # Difference in Draw Ratios
    df['win_ratio_difference'] = df['home_win_ratio'] - df['away_win_ratio']

    # # Home and Away Draw Ratios
    # df['home_draw_ratio'] = df.groupby('home')['home_recent_form'].transform(lambda x: np.mean(x == 1))
    # df['away_draw_ratio'] = df.groupby('away')['away_recent_form'].transform(lambda x: np.mean(x == 1))
    #
    # # Difference in Draw Ratios
    # df['draw_ratio_difference'] = df['home_draw_ratio'] - df['away_draw_ratio']
    #
    # # Home and Away Loss Ratios
    # df['home_loss_ratio'] = df.groupby('home')['home_recent_form'].transform(lambda x: np.mean(x == 0))
    # df['away_loss_ratio'] = df.groupby('away')['away_recent_form'].transform(lambda x: np.mean(x == 0))
    #
    # # Difference in Loss Ratios
    # df['loss_ratio_difference'] = df['home_loss_ratio'] - df['away_loss_ratio']

    # total shots
    df['home_shots'] = df['home_shots_on_target'] + df['home_shots_wide_of_target']
    df['away_shots'] = df['away_shots_on_target'] + df['away_shots_wide_of_target']

    # Home and Away Shots Ratio
    df['home_shots_ratio'] = df['home_shots'] / np.where((df['away_shots'] + df['home_shots']) == 0, 1,
                                                         (df['away_shots'] + df['home_shots']))
    df['away_shots_ratio'] = df['away_shots'] / np.where((df['away_shots'] + df['home_shots']) == 0, 1,
                                                         (df['away_shots'] + df['home_shots']))

    # Home and Away Shots on Target Ratios
    df['home_shots_on_target_ratio'] = df['home_shots_on_target'] / np.where(df['home_shots'] == 0, 1, df['home_shots'])
    df['away_shots_on_target_ratio'] = df['away_shots_on_target'] / np.where(df['away_shots'] == 0, 1, df['away_shots'])

    # Difference in Shots on Target Ratios
    df['shots_on_target_ratio_difference'] = df['home_shots_on_target_ratio'] - df['away_shots_on_target_ratio']

    return df


if retrain_model:

    match_data = parse_match_list(match_list_location)[:max_amount_of_training_matches]
    print(len(match_data))
    df = pd.DataFrame([data.__dict__ for data in match_data])

    df = add_new_colls(df, rename_teams=True).sort_index(axis=1)

    # Assuming you have a DataFrame called 'data' containing your features and target variable
    X = df.drop(['home_score', 'away_score', 'Div', 'Date', 'Time', 'final_time_result', 'source_file'], axis=1)
    y_home = df['home_score']
    y_away = df['away_score']

    # Split the data into training and testing sets
    X_train, X_test, y_train_home, y_test_home, y_train_away, y_test_away = train_test_split(X, y_home, y_away)

    # Train separate models for home and away scores
    model_home = RandomForestRegressor(n_estimators=estimators)
    model_home.fit(X_train, y_train_home)

    model_away = RandomForestRegressor(n_estimators=estimators)
    model_away.fit(X_train, y_train_away)

    # Save the models
    joblib.dump(model_home, 'nnmodels/randomForestRegressor/model_home.pkl')
    joblib.dump(model_away, 'nnmodels/randomForestRegressor/model_away.pkl')

    # Evaluate the models
    y_pred_home = model_home.predict(X_test)
    y_pred_away = model_away.predict(X_test)

    mse_home = mean_squared_error(y_test_home, y_pred_home)
    mse_away = mean_squared_error(y_test_away, y_pred_away)

    print(f"Mean Squared Error (Home Score): {mse_home}")
    print(f"Mean Squared Error (Away Score): {mse_away}")
    print("\n\n")

home_models = ['nnmodels/randomForestRegressor/model_home.pkl']
away_models = ['nnmodels/randomForestRegressor/model_away.pkl']


def silent_print(silent_inp, text):
    if not silent_inp:
        print(text)


def add_noise_to_features(X, noise_level):
    X_noisy = X.copy()
    for col in X_noisy.columns:
        if col not in ['home', 'away', 'home_score', 'away_score']:  # Ensure team names columns are not modified
            noise = np.random.uniform(-noise_level, noise_level, X_noisy[col].shape)
            X_noisy[col] += noise
            X_noisy[col] = X_noisy[col].clip(lower=0)  # Cap the values at 0
    return X_noisy


def predict(X_new, title, noise=False, amount_of_predictions=1):
    correct_ones = 0
    GD_correct = 0
    winner_correct = 0

    print("#" * (len(title) + 6))
    print("#  " + title + "  #")
    print("#" * (len(title) + 6))

    for j in range(amount_of_predictions):
        if noise:
            # Perturb input features with random noise
            X_new_noisy = add_noise_to_features(X_new, noise_level)
        else:
            X_new_noisy = X_new.copy()

        home_score_prediction = model_home.predict(X_new_noisy)
        away_score_prediction = model_away.predict(X_new_noisy)

        for i in range(len(home_score_prediction)):
            home_team_name = list(codes.keys())[list(codes.values()).index(int(new_data['home'].iloc[i]))]
            away_team_name = list(codes.keys())[list(codes.values()).index(int(new_data['away'].iloc[i]))]

            silent_print(silent,
                         f"Predicted Home Score for data point {i} ({home_team_name}): {home_score_prediction[i]}"
                         f" (Rounded down: {int(home_score_prediction[i])})")
            silent_print(silent,
                         f"Predicted Away Score for data point {i} ({away_team_name}): {away_score_prediction[i]}"
                         f" (Rounded down: {int(away_score_prediction[i])})")

            actual_home_score = y_home_new[i]
            actual_away_score = y_away_new[i]

            silent_print(silent, f"Actual Home Score for data point {i}: {actual_home_score}")
            silent_print(silent, f"Actual Away Score for data point {i}: {actual_away_score}")

            # Check if predicted scores match actual scores
            if int(home_score_prediction[i]) == actual_home_score:
                silent_print(silent, "Predicted Home Score matches actual Home Score!")
            else:
                silent_print(silent, "Predicted Home Score does not match actual Home Score!")

            if int(away_score_prediction[i]) == actual_away_score:
                silent_print(silent, "Predicted Away Score matches actual Away Score!")
            else:
                silent_print(silent, "Predicted Away Score does not match actual Away Score!")

            if (int(home_score_prediction[i]) - int(away_score_prediction[i])) == (
                    actual_home_score - actual_away_score):
                silent_print(silent, "Predicted GD matches actual GD!")
                GD_correct += 1
            else:
                silent_print(silent, "Predicted GD does not match actual GD!")

            if int(home_score_prediction[i]) == actual_home_score and int(
                    away_score_prediction[i]) == actual_away_score:
                silent_print(silent, "Predicted exact correct!")
                correct_ones += 1

            if int(home_score_prediction[i]) < int(
                    away_score_prediction[i]) and actual_home_score < actual_away_score or int(
                home_score_prediction[i]) > int(
                away_score_prediction[i]) and actual_home_score > actual_away_score or int(
                home_score_prediction[i]) == int(away_score_prediction[i]) and actual_home_score == actual_away_score:
                silent_print(silent, "Predicted winner correct!")
                winner_correct += 1
            silent_print(silent, "\n")

    amount_of_matches = len(y_home_new) * amount_of_predictions
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
    print("\n\n")


for model_home_path, model_away_path in zip(home_models, away_models):
    print("#" * (len(model_home_path) + len(model_away_path) + 23))
    print("#  home: " + model_home_path + " and away: " + model_away_path + "  #")
    print("#" * (len(model_home_path) + len(model_away_path) + 23))

    # Load the models
    model_home = joblib.load('nnmodels/randomForestRegressor/model_home.pkl')
    model_away = joblib.load('nnmodels/randomForestRegressor/model_away.pkl')

    # Make predictions
    new_data = pd.read_csv("input_data/toPredict.csv")  # Your new data for prediction
    new_data.columns = new_data.columns.map(lambda x: x.strip() if isinstance(x, str) else x)

    new_data = add_new_colls(new_data).sort_index(axis=1)  # add the columns we make from the data

    X_new = new_data.drop(['home_score', 'away_score'], axis=1)
    y_home_new = new_data['home_score']
    y_away_new = new_data['away_score']

    predict(X_new, "normal", amount_of_predictions=amount_of_non_noisy_predictions)
    predict(X_new, "noisy", True, amount_of_predictions=amount_of_noisy_predictions)
