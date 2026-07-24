import pandas as pd

def normalize_ticker(df):
    if "id" in df.columns:
        df["id"] = df["id"].astype(str).str.strip().str.upper()
    return df


def normalize_year(df):
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")
    return df