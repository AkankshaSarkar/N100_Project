import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DB_PATH = Path("db/nifty100.db")

conn = sqlite3.connect(DB_PATH)

query = """
   SELECT
    f.*,
    s.broad_sector,
    s.sub_sector,
    p.peer_group_name
FROM financial_ratios f
LEFT JOIN sectors s
ON f.company_id = s.company_id

LEFT JOIN peer_groups p
ON f.company_id = p.company_id
"""

df = pd.read_sql_query(query, conn)

print(df.head())
print(df.columns.tolist())
print(df["peer_group_name"].value_counts(dropna=False))

# NaN peer groups hata do
df = df[df["peer_group_name"].notna()]
print("Rows after removing NaN:", len(df))

print(df[["company_id", "peer_group_name", "return_on_equity_pct"]].head(10))

df["roe_rank"] = (
    df.groupby("peer_group_name")["return_on_equity_pct"]
      .rank(pct=True)
)

print(
    df[
        [
            "company_id",
            "peer_group_name",
            "return_on_equity_pct",
            "roe_rank"
        ]
    ].head(20)
)

output_path = "output/peer_percentile.csv"

df.to_csv(output_path, index=False)

print(f"File saved successfully: {output_path}")
conn.close()