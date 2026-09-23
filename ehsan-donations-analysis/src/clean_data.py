"""
clean_data.py
-------------
Reads the three raw quarterly donation CSVs exported from the Ehsan
platform (2024, 2025, 2026 - each with a slightly different layout/header
mess) and produces one clean, tidy dataset:

    data/processed/combined_clean.csv

Columns: year, quarter (Q1-Q4), indicator (Arabic), quarter_ar,
         raw_value, num_value, unit
"""
import re
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

QUARTER_MAP = {"الأول": "Q1", "الثاني": "Q2", "الثالث": "Q3", "الرابع": "Q4"}


def parse_value(raw: str):
    """Split a value like ' جمعية 183' or '1770403356 ريال' into (number, unit)."""
    raw = str(raw)
    nums = re.findall(r"\d+", raw.replace(",", ""))
    number = int("".join(nums)) if nums else None
    unit = re.sub(r"[\d,]", "", raw).strip()
    return number, unit


def load_2024(path: Path) -> pd.DataFrame:
    # File has a 6-line template preamble before the real header row.
    df = pd.read_csv(path, encoding="utf-8-sig", skiprows=6, header=None)
    df.columns = ["year", "quarter", "indicator", "value"]
    return df


def load_2025(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = ["year", "quarter", "indicator", "value"]
    return df.dropna(how="all")


def load_2026(path: Path) -> pd.DataFrame:
    # File has a stray leading empty column and two trailing empty columns.
    df = pd.read_csv(path, encoding="utf-8-sig")
    df = df.drop(columns=[df.columns[0], "Unnamed: 5", "Unnamed: 6"])
    df.columns = ["year", "quarter", "indicator", "value"]
    return df.dropna(how="all")


def main():
    df24 = load_2024(RAW_DIR / "donations_2024.csv")
    df25 = load_2025(RAW_DIR / "donations_2025.csv")
    df26 = load_2026(RAW_DIR / "donations_2026.csv")

    full = pd.concat([df24, df25, df26], ignore_index=True)
    full["year"] = full["year"].astype(int)
    full["quarter"] = full["quarter"].astype(str).str.strip()
    full["indicator"] = full["indicator"].astype(str).str.strip()
    full["quarter_code"] = full["quarter"].map(QUARTER_MAP)

    full[["num_value", "unit"]] = full["value"].apply(
        lambda v: pd.Series(parse_value(v))
    )
    full = full.rename(columns={"value": "raw_value"})

    out_path = OUT_DIR / "combined_clean.csv"
    full.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"Wrote {len(full)} rows -> {out_path}")


if __name__ == "__main__":
    main()
