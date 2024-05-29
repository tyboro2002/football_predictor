import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def visualize_position_chances(data, save_location, League):
    # Convert the data to a DataFrame
    df = pd.DataFrame(data, index=[f'Position {i + 1}' for i in range(len(League.teams))])

    # Create a heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.T, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title("Probability of Teams Finishing in Each Position")
    plt.xlabel("Position")
    plt.ylabel("Team")

    # Save the figure
    plt.savefig(save_location)
