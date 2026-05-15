# Egyptian Premier League 2025/26 - Probabilistic Title Race Model

A Poisson-based match outcome model built to estimate the probability of each team winning the Egyptian Premier League title in the final round of the Championship Stage (Round 7).

Built as a companion to a LinkedIn series on football analytics and statistics.

---

## Context

The 2025/26 Egyptian Premier League Championship Stage saw three teams competing for the title heading into the final matchday:

- Zamalek — 53 points
- Pyramids — 51 points
- Al Ahly — 50 points

Each team had one match remaining, all played simultaneously on 20/05/2026.

---

## Methodology

The model uses a classical Double Poisson approach for football match prediction:

1. Compute each team's attack strength and defensive weakness from season-long goals scored and conceded, normalized by the league average.
2. Estimate expected goals (xG) for each match using the attacking strength of one team against the defensive weakness of the other.
3. Use the Poisson distribution with xG as lambda to generate a full scoreline probability matrix for each match.
4. Aggregate scoreline probabilities into win/draw/loss outcomes for each match.
5. Multiply the relevant outcome probabilities across the three simultaneous matches to estimate the title probability for each scenario, assuming match independence.

---

## Data

All data sourced from Sofascore. Covers the full season (25 matches per team in the Championship Stage).

| File | Description |
|------|-------------|
| 1_season_stats.csv | Full season stats per team (goals, possession, clean sheets) |
| 2_championship_stats.csv | Championship round stats, form, and win percentage |
| 3_championship_matches.csv | Match-level results for all Championship Stage games |
| 4_h2h_round7.csv | Head-to-head records for the three Round 7 matchups |

---

## Results

| Match | Home xG | Away xG | Home Win | Draw | Away Win |
|-------|---------|---------|----------|------|----------|
| Al Masry vs Al Ahly | 0.95 | 1.28 | 27.6% | 28.3% | 44.1% |
| Zamalek vs Ceramica | 0.86 | 0.65 | 37.9% | 36.2% | 25.9% |
| Pyramids vs Smouha | 0.97 | 0.50 | 46.1% | 35.5% | 18.4% |

Title probabilities (assuming match independence):

- Al Ahly wins title: 6.1%
- Zamalek wins title: dominant favorite
- Pyramids wins title: second most likely

---

## Limitations

- Goals are assumed to be independent Poisson processes. In reality, goals are correlated through game state, red cards, and tactical adjustments.
- Match outcomes are assumed independent of each other.
- The model uses season-long averages and does not account for recent form weighting, injuries, or fatigue.
- Head-to-head records were used qualitatively as context and are not direct inputs to the Poisson model.
- A Dixon-Coles correction for low-scoring scorelines was not applied.

---

## File Structure

```
.
├── README.md
├── poisson_model.py
├── data/
│   ├── 1_season_stats.csv
│   ├── 2_championship_stats.csv
│   ├── 3_championship_matches.csv
│   └── 4_h2h_round7.csv
```

---

## Requirements

```
python 3.x
math (standard library)
csv (standard library)
```

No external dependencies required.

---

## Related

This model is part of a LinkedIn series on statistics and football analytics covering combinatorial probability, probabilistic modeling, Bayesian inference, and Monte Carlo simulation.
