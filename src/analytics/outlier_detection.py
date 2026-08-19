import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd


DB_PATH = Path("db/nifty100.db")
OUTPUT_PATH = Path("output/outlier_report.csv")


def generate_outlier_report():
    conn = sqlite3.connect(DB_PATH)

    query = """
    WITH latest AS (
        SELECT
            company_id,
            MAX(year) AS year
        FROM financial_ratios
        GROUP BY company_id
    )

    SELECT
        c.id AS company_id,
        c.company_name,
        s.broad_sector,
        fr.year,

        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.interest_coverage,
        fr.net_profit_margin_pct,
        fr.operating_profit_margin_pct,
        fr.free_cash_flow_cr,
        fr.earnings_per_share,
        fr.book_value_per_share

    FROM financial_ratios fr

    JOIN latest l
        ON fr.company_id = l.company_id
        AND fr.year = l.year

    JOIN companies c
        ON fr.company_id = c.id

    LEFT JOIN sectors s
        ON c.id = s.company_id

    WHERE s.broad_sector IS NOT NULL
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    print(f"Companies available for outlier detection: {len(df)}")

    metrics = [
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "revenue_cagr_5yr",
        "fcf_cagr_5yr",
        "free_cash_flow_cr",
        "earnings_per_share",
        "book_value_per_share",
    ]

    outliers = []

    for metric in metrics:

        if metric not in df.columns:
            print(f"Skipping missing metric: {metric}")
            continue

        # Convert metric to numeric
        df[metric] = pd.to_numeric(df[metric], errors="coerce")

        # Sector-wise mean and standard deviation
        sector_mean = df.groupby("broad_sector")[metric].transform("mean")
        sector_std = df.groupby("broad_sector")[metric].transform("std")

        # Z-score
        z_score = (df[metric] - sector_mean) / sector_std

        # Absolute Z-score > 3 = outlier
        mask = z_score.abs() > 3

        temp = df.loc[
            mask,
            [
                "company_id",
                "company_name",
                "broad_sector",
                "year",
            ]
        ].copy()

        temp["field"] = metric
        temp["value"] = df.loc[mask, metric]
        temp["z_score"] = z_score.loc[mask]
        temp["absolute_z_score"] = z_score.loc[mask].abs()

        outliers.append(temp)

    if outliers:
        result = pd.concat(outliers, ignore_index=True)

        result = result.sort_values(
            "absolute_z_score",
            ascending=False
        )

    else:
        result = pd.DataFrame(
            columns=[
                "company_id",
                "company_name",
                "broad_sector",
                "year",
                "field",
                "value",
                "z_score",
                "absolute_z_score",
            ]
        )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    result.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"Saved: {OUTPUT_PATH}"
    )

    print(
        f"Outlier rows: {len(result)}"
    )

    return result


if __name__ == "__main__":
    generate_outlier_report()