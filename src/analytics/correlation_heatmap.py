import sqlite3
from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# =========================================================
# Paths
# =========================================================

DB_PATH = Path("db/nifty100.db")
OUTPUT_PATH = Path("reports/correlation_heatmap.png")


# =========================================================
# KPI columns
# =========================================================

KPI_COLUMNS = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "net_profit_margin_pct",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "capex_cr",
    "earnings_per_share",
    "dividend_payout_ratio_pct",
]


def generate_correlation_heatmap():
    """
    Generate Pearson correlation heatmap for the latest
    financial KPI data across Nifty 100 companies.
    """

    # Create output directory if needed
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------------------------------
    # Database connection
    # -----------------------------------------------------

    conn = sqlite3.connect(DB_PATH)

    try:

        # -------------------------------------------------
        # Get latest financial year for each company
        # -------------------------------------------------

        query = """
        SELECT
            fr.company_id,
            fr.year,
            fr.return_on_equity_pct,
            fr.debt_to_equity,
            fr.operating_profit_margin_pct,
            fr.net_profit_margin_pct,
            fr.interest_coverage,
            fr.asset_turnover,
            fr.free_cash_flow_cr,
            fr.capex_cr,
            fr.earnings_per_share,
            fr.dividend_payout_ratio_pct

        FROM financial_ratios fr

        INNER JOIN (
            SELECT
                company_id,
                MAX(year) AS latest_year
            FROM financial_ratios
            GROUP BY company_id
        ) latest

        ON fr.company_id = latest.company_id
        AND fr.year = latest.latest_year
        """

        df = pd.read_sql_query(
            query,
            conn
        )

    finally:
        conn.close()

    # -----------------------------------------------------
    # Validate data
    # -----------------------------------------------------

    if df.empty:
        raise ValueError(
            "No financial ratio data available."
        )

    print(
        f"Companies available for correlation: {df['company_id'].nunique()}"
    )

    # -----------------------------------------------------
    # Convert KPI columns to numeric
    # -----------------------------------------------------

    for column in KPI_COLUMNS:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # -----------------------------------------------------
    # Select KPI data
    # -----------------------------------------------------

    kpi_df = df[KPI_COLUMNS].copy()

    # Remove columns with no usable data
    kpi_df = kpi_df.dropna(
        axis=1,
        how="all"
    )

    # -----------------------------------------------------
    # Pearson correlation
    # -----------------------------------------------------

    correlation = kpi_df.corr(
        method="pearson"
    )

    # -----------------------------------------------------
    # Plot heatmap
    # -----------------------------------------------------

    plt.figure(
        figsize=(14, 10)
    )

    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=0.5
    )

    plt.title(
        "Pearson Correlation Heatmap - Nifty 100 Financial KPIs"
    )

    plt.tight_layout()

    # -----------------------------------------------------
    # Save report
    # -----------------------------------------------------

    plt.savefig(
        OUTPUT_PATH,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved: {OUTPUT_PATH}"
    )

    print(
        f"Correlation matrix shape: {correlation.shape}"
    )


if __name__ == "__main__":
    generate_correlation_heatmap()