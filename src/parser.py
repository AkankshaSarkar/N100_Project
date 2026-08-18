import re
from pathlib import Path
import pandas as pd


# Input and output paths
INPUT_FILE = Path("Data/raw/analysis.xlsx")
OUTPUT_FILE = Path("output/analysis_parsed.csv")
FAILURE_FILE = Path("output/parse_failures.csv")


# Example:
# "10 Years: 21%"
# "5 Years: 24%"
# "3 Years: 17%"
PATTERN = re.compile(
    r"(\d+)\s*Years?\s*:?\s*(-?\d+(?:\.\d+)?)\s*%"
)


def parse_analysis():

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Row 1 of Excel contains the actual column headers
    df = pd.read_excel(INPUT_FILE, header=1)

    parsed_rows = []
    failures = []

    # Required metric columns
    metric_columns = [
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe"
    ]

    for _, row in df.iterrows():

        company_id = str(row["company_id"]).strip()

        for metric in metric_columns:

            if metric not in df.columns:
                continue

            value = row[metric]

            if pd.isna(value):
                continue

            text = str(value).strip()

            # Find values like "10 Years: 21%"
            matches = PATTERN.findall(text)

            for period_years, value_pct in matches:

                parsed_rows.append({
                    "company_id": company_id,
                    "metric_type": metric,
                    "period_years": int(period_years),
                    "value_pct": float(value_pct)
                })

            # Ignore TTM / Last Year because the task requires
            # period_years extracted from "X Years: Y%"
            if text and not matches:
                if not (
                    text.startswith("TTM")
                    or text.startswith("Last Year")
                ):
                    failures.append({
                        "company_id": company_id,
                        "metric_type": metric,
                        "text": text
                    })

    # Create parsed dataframe
    parsed_df = pd.DataFrame(
        parsed_rows,
        columns=[
            "company_id",
            "metric_type",
            "period_years",
            "value_pct"
        ]
    )

    # Save parsed output
    parsed_df.to_csv(OUTPUT_FILE, index=False)

    # Save failures
    failure_df = pd.DataFrame(
        failures,
        columns=[
            "company_id",
            "metric_type",
            "text"
        ]
    )

    failure_df.to_csv(FAILURE_FILE, index=False)

    print("===================================")
    print("ANALYSIS PARSER COMPLETE")
    print("===================================")
    print(f"Parsed records : {len(parsed_df)}")
    print(f"Parse failures : {len(failure_df)}")
    print(f"Saved          : {OUTPUT_FILE}")
    print(f"Saved          : {FAILURE_FILE}")

    print("\nFirst 10 parsed records:")
    print(parsed_df.head(10).to_string(index=False))


if __name__ == "__main__":
    parse_analysis()