import sqlite3
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

from pathlib import Path

DB_PATH = Path("db/nifty100.db")

conn = sqlite3.connect(DB_PATH)

query = """
PRAGMA table_info(financial_ratios);
"""

df = pd.read_sql_query(query, conn)

print(df)

df.to_csv("output/query_output.csv", index=False)
print("Output saved successfully.")

conn.close()