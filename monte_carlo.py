import math
import random

random.seed(42)

# ============================================================
# Egyptian Premier League 2025/26 - Championship Stage
# Monte Carlo Title Race Simulation — Round 7
# Data source: Sofascore (25 matches per team, full season)
# ============================================================

# Season stats
teams = {
    "Al Ahly":            {"gf": 42, "ga": 24, "matches": 25},
    "Zamalek":            {"gf": 38, "ga": 17, "matches": 25},
    "Pyramids":           {"gf": 41, "ga": 20, "matches": 25},
    "Ceramica Cleopatra": {"gf": 34, "ga": 20, "matches": 25},
    "Al Masry":           {"gf": 35, "ga": 27, "matches": 25},
    "Smouha":             {"gf": 22, "ga": 21, "matches": 25},
}

# ============================================================
# Step 1: League average and team strengths
# ============================================================
total_goals   = sum(t["gf"] for t in teams.values())
total_matches = sum(t["matches"] for t in teams.values())
league_avg    = total_goals / total_matches

for team, stats in teams.items():
    stats["attack"]  = (stats["gf"] / stats["matches"]) / league_avg
    stats["defense"] = (stats["ga"] / stats["matches"]) / league_avg

# ============================================================
# Step 2: Poisson sampler
# ============================================================
def poisson_sample(lam):
    """Sample from Poisson distribution using Knuth's algorithm."""
    L, k, p = math.exp(-lam), 0, 1.0
    while p > L:
        k += 1
        p *= random.random()
    return k - 1

def simulate_match(home, away):
    """Simulate a match and return (home_goals, away_goals)."""
    home_xg = teams[home]["attack"] * teams[away]["defense"] * league_avg
    away_xg = teams[away]["attack"] * teams[home]["defense"] * league_avg
    return poisson_sample(home_xg), poisson_sample(away_xg)

# ============================================================
# Step 3: Tiebreaker rules
# Head-to-head record between the top 3 (this season):
#   Al Ahly beat Zamalek twice
#   Pyramids beat Al Ahly twice
#   Zamalek beat Pyramids twice
# -> Three-way H2H is a perfect cycle, so goal difference decides
# ============================================================
h2h_wins = {
    ("Al Ahly", "Zamalek"):  2,
    ("Zamalek", "Al Ahly"):  0,
    ("Pyramids", "Al Ahly"): 2,
    ("Al Ahly", "Pyramids"): 0,
    ("Zamalek", "Pyramids"): 2,
    ("Pyramids", "Zamalek"): 0,
}

def h2h_winner(t1, t2):
    w1 = h2h_wins.get((t1, t2), 0)
    w2 = h2h_wins.get((t2, t1), 0)
    if w1 > w2: return t1
    if w2 > w1: return t2
    return None

def resolve_title(pts, gf, ga):
    """
    Determine title winner using:
    1. Points
    2. Head-to-head record (two-way ties only)
    3. Goal difference
    4. Goals scored
    """
    max_pts = max(pts.values())
    winners = [t for t, p in pts.items() if p == max_pts]

    if len(winners) == 1:
        return winners[0]

    # Two-way tie: check H2H first
    if len(winners) == 2:
        t1, t2 = winners
        hw = h2h_winner(t1, t2)
        if hw:
            return hw
        # H2H equal -> goal difference
        gd = {t: gf[t] - ga[t] for t in winners}
        if gd[t1] != gd[t2]:
            return max(winners, key=lambda t: gd[t])
        # Goal difference equal -> goals scored
        if gf[t1] != gf[t2]:
            return max(winners, key=lambda t: gf[t])
        return "two_way_draw"

    # Three-way tie: H2H is a cycle -> go straight to goal difference
    gd = {t: gf[t] - ga[t] for t in winners}
    max_gd = max(gd.values())
    gd_winners = [t for t in winners if gd[t] == max_gd]
    if len(gd_winners) == 1:
        return gd_winners[0]
    # Goal difference equal -> goals scored
    max_gf = max(gf[t] for t in gd_winners)
    gf_winners = [t for t in gd_winners if gf[t] == max_gf]
    if len(gf_winners) == 1:
        return gf_winners[0]
    return "three_way_draw"

# ============================================================
# Step 4: Monte Carlo simulation
# ============================================================
N = 100_000

title_counts = {
    "Al Ahly": 0, "Zamalek": 0, "Pyramids": 0,
    "two_way_draw": 0, "three_way_draw": 0
}

# Points and goals before Round 7
points_before = {"Zamalek": 53, "Pyramids": 51, "Al Ahly": 50}
season_gf     = {"Al Ahly": 42, "Zamalek": 38, "Pyramids": 41}
season_ga     = {"Al Ahly": 24, "Zamalek": 17, "Pyramids": 20}

for _ in range(N):
    # Simulate Round 7
    hg1, ag1 = simulate_match("Al Masry", "Al Ahly")            # Al Ahly away
    hg2, ag2 = simulate_match("Zamalek", "Ceramica Cleopatra")
    hg3, ag3 = simulate_match("Pyramids", "Smouha")

    # Update points
    pts = {
        "Al Ahly":  points_before["Al Ahly"]  + (3 if ag1>hg1 else 1 if ag1==hg1 else 0),
        "Zamalek":  points_before["Zamalek"]  + (3 if hg2>ag2 else 1 if hg2==ag2 else 0),
        "Pyramids": points_before["Pyramids"] + (3 if hg3>ag3 else 1 if hg3==ag3 else 0),
    }

    # Update goals
    gf = {
        "Al Ahly":  season_gf["Al Ahly"]  + ag1,
        "Zamalek":  season_gf["Zamalek"]  + hg2,
        "Pyramids": season_gf["Pyramids"] + hg3,
    }
    ga = {
        "Al Ahly":  season_ga["Al Ahly"]  + hg1,
        "Zamalek":  season_ga["Zamalek"]  + ag2,
        "Pyramids": season_ga["Pyramids"] + ag3,
    }

    winner = resolve_title(pts, gf, ga)
    title_counts[winner] += 1

# ============================================================
# Step 5: Results
# ============================================================
print(f"Monte Carlo Simulation — {N:,} runs")
print("=" * 45)
for team in ["Zamalek", "Pyramids", "Al Ahly", "two_way_draw", "three_way_draw"]:
    pct = title_counts[team] / N * 100
    print(f"{team:25} {pct:6.2f}%")
