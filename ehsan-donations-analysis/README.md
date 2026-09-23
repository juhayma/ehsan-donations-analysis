# Ehsan Platform — Quarterly Donations Analysis & Ramadan Effect

Analysis of quarterly donation data from the Saudi Ehsan platform (2024–2026) to test whether Ramadan has a measurable effect on donations, and to forecast donations for the next Ramadan (1448H, expected February 2027).

## Methodology & Technical Environment

- **Data Processing:** `pandas` and `numpy` for data ingestion, cleaning, handling missing variables, and time-series aggregation.
- **Visualization:** `matplotlib` for generating static, analytical plots.
- **Forecasting Approach:** Extrapolation based on Compound Annual Growth Rate (CAGR) and Year-over-Year (YoY) averages strictly applied to Q1 historical subsets.

## Data

Raw files in `data/raw/` (as provided by Ehsan, one messy CSV per year):

| File | Years covered | Notes |
|---|---|---|
| `donations_2024.csv` | 2024, Q1–Q4 | Has a template preamble before the real header |
| `donations_2025.csv` | 2025, Q1–Q4 | Cleanest of the three |
| `donations_2026.csv` | 2026, Q1–Q2 only | Year in progress; extra empty columns |

Each row is one `(year, quarter, indicator, value)` observation. 11 indicators per quarter: total donations, number of associations added, number of transactions, number/value of completed projects, and campaign metrics.

### Ramadan ↔ Gregorian quarter mapping (Umm al-Qura calendar)

Ramadan shifts ~11 days earlier each Gregorian year. For the years in this dataset it happens to fall (almost) entirely inside **Q1** every time:

| Hijri year | Ramadan dates | Gregorian quarter |
|---|---|---|
| 1445H | 11 Mar – 9 Apr 2024 | Q1 2024 (spills a few days into Q2) |
| 1446H | 1 Mar – 30 Mar 2025 | Entirely in Q1 2025 |
| 1447H | 18 Feb – 19 Mar 2026 | Entirely in Q1 2026 |
| 1448H | ~7–8 Feb 2027 (est.) | Entirely in Q1 2027 — **forecast target** |

## Reproducibility

To replicate this analysis and regenerate the outputs locally, ensure a Python 3.8+ environment and run the pipeline sequentially:

```bash
git clone [https://github.com/yourusername/ehsan-donations-analysis.git](https://github.com/yourusername/ehsan-donations-analysis.git)
cd ehsan-donations-analysis
pip install -r requirements.txt

# 1. Ingest, clean, and merge raw temporal data
python src/clean_data.py

# 2. Execute statistical analysis and calculate forecasts
python src/analyze.py

# 3. Generate publication-ready visualizations
python src/visualize.py
