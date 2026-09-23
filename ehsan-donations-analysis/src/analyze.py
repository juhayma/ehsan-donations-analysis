"""
analyze.py
----------
Loads data/processed/combined_clean.csv and:

1. Builds quarterly pivot tables for the key indicators.
2. Tests whether Q1 (the quarter Ramadan falls in every year in this
   dataset) is systematically higher than the other quarters.
3. Forecasts Q1 2027 (Ramadan 1448H) using two simple methods:
   average YoY growth and CAGR, applied to Q1 2026.

Ramadan (Hijri) <-> Gregorian mapping used for interpretation
(source: Umm al-Qura calendar):
    Ramadan 1445H ~ 11 Mar - 9 Apr 2024   -> mostly inside 2024-Q1 (spills into Q2)
    Ramadan 1446H ~  1 Mar - 30 Mar 2025  -> entirely inside 2025-Q1
    Ramadan 1447H ~ 18 Feb - 19 Mar 2026  -> entirely inside 2026-Q1
    Ramadan 1448H ~ expected ~7-8 Feb 2027 -> entirely inside 2027-Q1 (forecast target)

NOTE ON LIMITATIONS: the source data is quarterly, not daily/monthly, so
Ramadan-specific spending cannot be isolated with certainty from the rest
of Q1. The analysis below treats "Q1 dominance" as strong circumstantial
evidence of a Ramadan effect, not as a precisely isolated measurement.
Forecasts are based on only 3 historical Q1 data points and should be
read as directional, not precise.
"""
import json
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
PROCESSED = BASE / "data" / "processed" / "combined_clean.csv"
OUT_DIR = BASE / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

INDICATORS = {
    "total_donations": "إجمالي التبرعات",
    "operations_count": "عدد العمليات",
    "associations_added": "عدد الجمعيات المضافة",
    "completed_projects_count": "عدد المشاريع المكتملة",
    "completed_projects_value": "قيمة المشاريع المكتملة",
    "campaign_donations_total": "مجموع التبرعات للحملات المنشئة",
    "campaigns_created": "عدد الحملات المنشئه",
}


def load():
    df = pd.read_csv(PROCESSED, encoding="utf-8-sig")
    return df


def pivot(df, indicator_ar):
    sub = df[df["indicator"] == indicator_ar]
    return sub.pivot(index="year", columns="quarter_code", values="num_value")


def forecast_q1_2027(q1_series: pd.Series):
    """q1_series indexed by year: 2024, 2025, 2026."""
    g1 = q1_series[2025] / q1_series[2024] - 1
    g2 = q1_series[2026] / q1_series[2025] - 1
    avg_growth = (g1 + g2) / 2
    cagr = (q1_series[2026] / q1_series[2024]) ** (1 / 2) - 1

    forecast_avg = q1_series[2026] * (1 + avg_growth)
    forecast_cagr = q1_series[2026] * (1 + cagr)
    low = q1_series[2026] * (1 + min(g1, g2))
    high = q1_series[2026] * (1 + max(g1, g2))

    return {
        "growth_2024_2025_pct": round(g1 * 100, 1),
        "growth_2025_2026_pct": round(g2 * 100, 1),
        "avg_growth_pct": round(avg_growth * 100, 1),
        "cagr_pct": round(cagr * 100, 1),
        "forecast_avg_growth_method": round(forecast_avg, 0),
        "forecast_cagr_method": round(forecast_cagr, 0),
        "forecast_range_low": round(low, 0),
        "forecast_range_high": round(high, 0),
    }


def ramadan_effect(donations_pivot, ops_pivot):
    results = {}
    for year in [2024, 2025]:  # only full years can give an annual share
        row = donations_pivot.loc[year]
        annual = row.sum()
        others_mean = row[["Q2", "Q3", "Q4"]].mean()
        results[year] = {
            "q1_share_of_year_pct": round(row["Q1"] / annual * 100, 1),
            "q1_vs_other_quarters_ratio": round(row["Q1"] / others_mean, 2),
        }

    avg_txn = donations_pivot / ops_pivot
    results["avg_donation_per_operation_SAR"] = avg_txn.round(1).to_dict()
    return results


def main():
    df = load()
    pivots = {name: pivot(df, ar) for name, ar in INDICATORS.items()}

    donations = pivots["total_donations"]
    ops = pivots["operations_count"]

    effect = ramadan_effect(donations, ops)
    forecast = forecast_q1_2027(donations["Q1"])

    forecasts_all = {}
    for name, piv in pivots.items():
        try:
            forecasts_all[name] = forecast_q1_2027(piv["Q1"])
        except Exception:
            pass

    results = {
        "pivots": {k: v.to_dict() for k, v in pivots.items()},
        "ramadan_effect": effect,
        "q1_2027_forecast_total_donations": forecast,
        "q1_2027_forecast_all_indicators": forecasts_all,
    }

    with open(OUT_DIR / "analysis_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    print(json.dumps(results["ramadan_effect"], ensure_ascii=False, indent=2))
    print(json.dumps(results["q1_2027_forecast_total_donations"], ensure_ascii=False, indent=2))
    print(f"\nFull results written to {OUT_DIR / 'analysis_results.json'}")


if __name__ == "__main__":
    main()
