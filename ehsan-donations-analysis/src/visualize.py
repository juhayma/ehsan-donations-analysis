"""
visualize.py
------------
Generates static PNG charts from the cleaned data + forecast results:

    outputs/figures/quarterly_donations.png
    outputs/figures/q1_forecast.png
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
PROCESSED = BASE / "data" / "processed" / "combined_clean.csv"
RESULTS = BASE / "outputs" / "analysis_results.json"
FIG_DIR = BASE / "outputs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def quarterly_donations_chart(df):
    sub = df[df["indicator"] == "إجمالي التبرعات"]
    piv = sub.pivot(index="year", columns="quarter_code", values="num_value") / 1e6

    fig, ax = plt.subplots(figsize=(8, 5))
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    x = range(len(quarters))
    width = 0.25
    colors = {2024: "#0e7c5a", 2025: "#c9a24b", 2026: "#8a5cf5"}

    for i, year in enumerate(piv.index):
        vals = [piv.loc[year, q] if q in piv.columns and not pd.isna(piv.loc[year, q]) else 0 for q in quarters]
        ax.bar([p + i * width for p in x], vals, width=width, label=str(year), color=colors.get(year))

    ax.set_xticks([p + width for p in x])
    ax.set_xticklabels(quarters)
    ax.set_ylabel("Total donations (million SAR)")
    ax.set_title("Ehsan platform - quarterly total donations (2024-2026)")
    ax.legend(title="Year")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "quarterly_donations.png", dpi=150)
    plt.close(fig)


def q1_forecast_chart(results):
    piv = results["pivots"]["total_donations"]["Q1"]
    q1_vals = [piv[y] / 1e6 for y in ["2024", "2025", "2026"]]
    forecast = results["q1_2027_forecast_total_donations"]["forecast_avg_growth_method"] / 1e6

    labels = ["Q1 2024", "Q1 2025", "Q1 2026", "Q1 2027\n(forecast)"]
    values = q1_vals + [forecast]
    colors = ["#0e7c5a", "#0e7c5a", "#0e7c5a", "#c9a24b"]

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(labels, values, color=colors)
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + 20, f"{v:,.0f}", ha="center", fontsize=9)
    ax.set_ylabel("Total donations (million SAR)")
    ax.set_title("Q1 (Ramadan quarter) donations - actual vs 2027 forecast")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "q1_forecast.png", dpi=150)
    plt.close(fig)


def main():
    df = pd.read_csv(PROCESSED, encoding="utf-8-sig")
    with open(RESULTS, encoding="utf-8") as f:
        results = json.load(f)

    quarterly_donations_chart(df)
    q1_forecast_chart(results)
    print(f"Charts written to {FIG_DIR}")


if __name__ == "__main__":
    main()
