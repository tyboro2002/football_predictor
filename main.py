from models.formats import League
from simulate import simulate_game, simulate_league
from visualize import visualize_position_chances

save_location = "results/league_probabilities.png"
amount_of_simulations = 100_000

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
        ("Kv mechelen", 8),
        ("Stvv", 9),
        ("Oh leuven", 10),
        ("Standard", 12),
        ("Charlerio", 13),
        ("Kv korterijk", 14),
        ("Rwdm", 15),
        ("Kas eupen", 16)
    ]
)

# print(JPL)
# for matchday in JPL.matchdays:
#     print(matchday)

# print(simulate_game(JPL.matchdays[0][0], 10))
data = simulate_league(JPL, amount_of_simulations)
print(data)

visualize_position_chances(data, save_location, JPL)


# print(predict_league(JPL))
