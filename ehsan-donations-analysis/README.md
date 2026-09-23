# Ehsan Platform — Quarterly Donations Analysis & Ramadan Effect

Analysis of quarterly donation data from the Saudi Ehsan platform (2024–2026)
to test whether Ramadan has a measurable effect on donations, and to forecast
donations for the next Ramadan (1448H, expected February 2027).

## Data

Raw files in `data/raw/` (as provided by Ehsan, one messy CSV per year):

| File | Years covered | Notes |
|---|---|---|
| `donations_2024.csv` | 2024, Q1–Q4 | Has a template preamble before the real header |
| `donations_2025.csv` | 2025, Q1–Q4 | Cleanest of the three |
| `donations_2026.csv` | 2026, Q1–Q2 only | Year in progress; extra empty columns |

Each row is one `(year, quarter, indicator, value)` observation. 11 indicators
per quarter: total donations, number of associations added, number of
transactions, number/value of completed projects, and campaign metrics.

### Ramadan ↔ Gregorian quarter mapping (Umm al-Qura calendar)

Ramadan shifts ~11 days earlier each Gregorian year. For the years in this
dataset it happens to fall (almost) entirely inside **Q1** every time:

| Hijri year | Ramadan dates | Gregorian quarter |
|---|---|---|
| 1445H | 11 Mar – 9 Apr 2024 | Q1 2024 (spills a few days into Q2) |
| 1446H | 1 Mar – 30 Mar 2025 | Entirely in Q1 2025 |
| 1447H | 18 Feb – 19 Mar 2026 | Entirely in Q1 2026 |
| 1448H | ~7–8 Feb 2027 (est.) | Entirely in Q1 2027 — **forecast target** |

## Pipeline

```bash
pip install -r requirements.txt
python src/clean_data.py    # raw CSVs -> data/processed/combined_clean.csv
python src/analyze.py       # -> outputs/analysis_results.json
python src/visualize.py     # -> outputs/figures/*.png
```

## Key findings

- **Q1 donations are consistently 2.2×–2.7× higher** than the average of the
  other three quarters, every single year in the dataset.
- Q1 represents **42% of the full year's donations in 2024** and **48% in
  2025**, despite being one of four quarters.
- The **average donation per transaction roughly doubles in Q1** (e.g. ~97 SAR
  vs ~33 SAR in 2024, ~58 SAR vs ~24 SAR in 2025), suggesting Ramadan brings
  fewer but larger transactions, not just more activity.
- This pattern repeats for three consecutive years with the same direction —
  consistent with Ramadan being the driver, though the data cannot prove
  causation on its own (see Limitations).

### Q1 2027 (Ramadan 1448H) forecast

| Method | Forecast (total donations) |
|---|---|
| Average YoY growth (16.8%) | ~2.81 billion SAR |
| CAGR 2024→2026 (16.7%) | ~2.81 billion SAR |
| Range (slow vs fast recent growth) | 2.68 – 2.95 billion SAR |

Full numbers (all indicators) are in `outputs/analysis_results.json`.

## Limitations

- **Quarterly, not daily/monthly data.** We cannot isolate Ramadan-specific
  days from the rest of Q1 — the "Ramadan effect" here is inferred from Q1
  dominance, not measured directly.
- **Only 3 data points per indicator** (2024, 2025, 2026). The forecast is
  directional, not a precise prediction — the YoY growth rate itself is
  slowing (22.5% → 11.1%), so a straight-line extrapolation carries real
  uncertainty.
- Ramadan length varies (29 or 30 days) and its exact position within Q1
  varies slightly year to year — not modeled here.

## Suggested next steps

- Get monthly or daily donation data to isolate Ramadan days precisely.
- Add more historical years to strengthen the forecast.
- Model campaign-level data (large one-off campaigns can skew a quarter
  independent of Ramadan).

## Project structure

```
.
├── data/
│   ├── raw/                 # original CSVs as provided
│   └── processed/           # cleaned, tidy combined dataset
├── src/
│   ├── clean_data.py
│   ├── analyze.py
│   └── visualize.py
├── outputs/
│   ├── analysis_results.json
│   └── figures/
├── requirements.txt
└── README.md
```
