from formats import generate_league_match_schedule, check_leauge
from predict import predict
from game import League, FootballGame

JPL = League(["club brugge", "kv oostende", "krc genk", "westerlo"])
print(JPL)
schedule = generate_league_match_schedule(JPL)
assert check_leauge(JPL, schedule)

playday = 1
for matchday in schedule:
    print("day", playday)
    playday += 1
    for match in matchday:
        prediction = predict(match)
        print(match.team1, "VS", match.team2, "results in", prediction)
        if prediction == match.team1:
            JPL.record_match_result(match.team1, match.team2, 1, 0)
        if prediction == "draw":
            JPL.record_match_result(match.team1, match.team2, 0, 0)
        if prediction == match.team2:
            JPL.record_match_result(match.team1, match.team2, 0, 1)
print(JPL)


