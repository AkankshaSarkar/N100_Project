import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("db/nifty100.db")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

tables = [
    "analysis",
    "balancesheet",
    "cashflow",
    "companies",
    "documents",
    "financial_ratios",
    "market_cap",
    "peer_groups",
    "profitandloss",
    "prosandcons",
    "sectors",
    "stock_prices"
]

audit = []

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]

    audit.append({
        "table_name": table,
        "row_count": count,
        "status": "Loaded"
    })

    audit_df = pd.DataFrame(audit)

audit_df.to_csv(
    OUTPUT_DIR / "load_audit.csv",
    index=False
)

print(audit_df)

failures = []

# Example validation: Empty companies table
cursor.execute("SELECT COUNT(*) FROM companies")
count = cursor.fetchone()[0]

if count == 0:
    failures.append({
        "rule": "Companies table not empty",
        "severity": "CRITICAL",
        "status": "FAIL"
    })
else:
    failures.append({
        "rule": "Companies table not empty",
        "severity": "INFO",
        "status": "PASS"
    })

failure_df = pd.DataFrame(failures)

failure_df.to_csv(
    OUTPUT_DIR / "validation_failures.csv",
    index=False
)

print(failure_df)




conn.close()