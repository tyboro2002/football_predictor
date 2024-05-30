from models.formats import League
from predict import predict_league
from simulate import simulate_league
from visualize import visualize_position_chances, visualize_league, visualize_league_matches, visualize_all_team_matches
import time

save_location = "results/league_probabilities.png"
save_location2 = "results/league1.png"
amount_of_simulations = 100


def get_matchday_location(day):
    return f"results/matchdays/matchday_{day}.png"


def get_team_location(team_name):
    return f"results/teams/{team_name}.png"


JPL = League(
    [
        ("Club brugge", (1,)),
        ("Union", (2,)),
        ("Anderlecht", (3,)),
        ("Cercle brugge", (4,)),
        ("Krc genk", (5,)),
        ("Antwerpen", (6,)),
        ("Gent", (7,)),
        ("Kv mechelen", (8,)),
        ("Stvv", (9,)),
        ("Oh leuven", (10,)),
        ("Westerlo", (11,)),
        ("Standard", (12,)),
        ("Charlerio", (13,)),
        ("Kv korterijk", (14,)),
        ("Rwdm", (15,)),
        ("Kas eupen", (16,))
    ]
)

# print(JPL.get_standings())
# for matchday in JPL.matchdays:
#     print(matchday)

# print(simulate_game(JPL.matchdays[0][0], 10))

if __name__ == '__main__':
    start_time = time.time()
    data = simulate_league(JPL, amount_of_simulations)
    end_time = time.time()

    print(f"Multiprocessing simulation time: {end_time - start_time} seconds")
    print("data", data)
    visualize_position_chances(data, save_location, JPL)
    predicted = predict_league(JPL)
    visualize_league(predicted, save_location2)
    visualize_league_matches(predicted, get_matchday_location)
    visualize_all_team_matches(predicted, get_team_location)

# print(predict_league(JPL))
