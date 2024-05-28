from formats import League
from simulate import simulate_game, simulate_league

JPL = League(["club brugge", "kv oostende", "krc genk", "westerlo"])


print(simulate_game(JPL.matchdays[0][0], 10))
print(simulate_league(JPL, 10))
