from models.formats import League
from simulate import simulate_game, simulate_league
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

save_location = "results/league_probabilities.png"

JPL = League(
    [
        ("Club brugge", 1),
        ("Union", 2),
        ("Anderlecht", 3),
        ("Krc genk", 5),
        ("Westerlo", 11),
        ("Antwerpen", 6),
        ("Cercle brugge", 4),
        ("Gent", 7),
        # ("Kv mechelen", 8),
        # ("Stvv", 9),
        # ("Oh leuven", 10),
        # ("Standard", 12),
        # ("Charlerio", 13),
        # ("Kv korterijk", 14),
        # ("Rwdm", 15),
        # ("Kas eupen", 16)
    ]
)

print(JPL)
for matchday in JPL.matchdays:
    print(matchday)

print(simulate_game(JPL.matchdays[0][0], 10))
data = simulate_league(JPL, 100)
print(data)

# Convert the data to a DataFrame
df = pd.DataFrame(data, index=[f'Position {i+1}' for i in range(8)])

# Create a heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(df.T, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title("Probability of Teams Finishing in Each Position")
plt.xlabel("Position")
plt.ylabel("Team")

# Save the figure
plt.savefig(save_location)

# print(predict_league(JPL))
