from formats import generate_league_match_schedule, check_leauge
import predict
from game import League, FootballGame

JPL = League(["club brugge", "kv oostende", "krc genk", "westerlo"])
print(JPL)
schedule = generate_league_match_schedule(JPL)
# for matchday in schedule:
#     print(matchday)

for i in range(0, 10_000):
    schedule = generate_league_match_schedule(JPL)
    if not check_leauge(JPL, schedule):
        print("fail")
print("all good")