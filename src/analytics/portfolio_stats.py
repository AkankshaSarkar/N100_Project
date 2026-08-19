import sqlite3
from pathlib import Path

import pandas as pd


DB_PATH = Path("db/nifty100.db")
OUTPUT_PATH = Path("output/portfolio_stats.csv")


def generate_portfolio_stats():
    """
    Generate P10, P25, P50, P75, P90, Mean and Std
    statistics for the 10 core KPIs across companies.
    """

    metrics = [
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "asset_turnover",
        "free_cash_flow_cr",
        "earnings_per_share",
        "book_value_per_share",
        "dividend_payout_ratio_pct",
    ]

    conn = sqlite3.connect(DB_PATH)

    # Get the latest financial year for every company
    query = """
    WITH latest AS (
        SELECT
            company_id,
            MAX(year) AS latest_year
        FROM financial_ratios
        GROUP BY company_id
    )
    SELECT
        fr.company_id,
        fr.year,
        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.interest_coverage,
        fr.net_profit_margin_pct,
        fr.operating_profit_margin_pct,
        fr.asset_turnover,
        fr.free_cash_flow_cr,
        fr.earnings_per_share,
        fr.book_value_per_share,
        fr.dividend_payout_ratio_pct
    FROM financial_ratios fr
    JOIN latest l
        ON fr.company_id = l.company_id
        AND fr.year = l.latest_year
    JOIN companies c
        ON fr.company_id = c.id
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    print(f"Companies available for portfolio statistics: {df['company_id'].nunique()}")

    results = []

    for metric in metrics:
        if metric not in df.columns:
            print(f"Skipping missing metric: {metric}")
            continue

        values = pd.to_numeric(df[metric], errors="coerce").dropna()

        if values.empty:
            continue

        results.append(
            {
                "metric": metric,
                "P10": values.quantile(0.10),
                "P25": values.quantile(0.25),
                "P50": values.quantile(0.50),
                "P75": values.quantile(0.75),
                "P90": values.quantile(0.90),
                "Mean": values.mean(),
                "Std": values.std(),
            }
        )

    result_df = pd.DataFrame(results)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved: {OUTPUT_PATH}")
    print(f"Statistics generated for: {len(result_df)} KPIs")
    print(result_df)


if __name__ == "__main__":
    generate_portfolio_stats()