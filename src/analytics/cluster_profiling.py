from pathlib import Path
import sqlite3

import pandas as pd
FEATURES = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "asset_turnover",
    "free_cash_flow_cr",
]
def run_cluster_profiling():
    db_path = Path("db/nifty100.db")
    cluster_file = Path("output/cluster_labels.csv")

    conn = sqlite3.connect(db_path)

    query = """
SELECT
    c.id AS company_id,
    c.company_name,
    fr.year,
    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.operating_profit_margin_pct,
    fr.asset_turnover,
    fr.free_cash_flow_cr
FROM companies c
JOIN financial_ratios fr
    ON c.id = fr.company_id
"""

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Keep latest available year for each company
    df = df.sort_values(["company_id", "year"])
    df = df.drop_duplicates(
        subset=["company_id"],
        keep="last",
    )

    # Load cluster assignments generated on Day 36
    clusters = pd.read_csv(cluster_file)

    df = df.merge(
        clusters[
            [
                "company_id",
                "cluster_id",
                "cluster_name",
            ]
        ],
        on="company_id",
        how="inner",
    )

    # Cluster-wise mean and median
    profile = (
    df.groupby(["cluster_id", "cluster_name"])[FEATURES]
      .agg(["mean", "median"])
      .round(4)
      .reset_index()
)

# Flatten MultiIndex columns
    profile.columns = [
    "_".join(col).strip("_") if isinstance(col, tuple) else col
    for col in profile.columns
]

    print("\n===== CLUSTER PROFILE =====\n")
    print(profile)

    # Save result
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "cluster_profile.csv"
    profile.to_csv(output_file, index=False)

    print("\nSaved:", output_file)

    return profile


if __name__ == "__main__":
    run_cluster_profiling()