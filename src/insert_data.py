import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("db/nifty100.db")
DATA_PATH = Path("Data/raw")

conn = sqlite3.connect(DB_PATH)

excel_files = DATA_PATH.glob("*.xlsx")

for file in excel_files:

    if file.stem.lower() == "companies":
        df = pd.read_excel(file, header=1)
    elif file.stem.lower() == "profitandloss":
        df = pd.read_excel(file, header=2)
    else:
        df = pd.read_excel(file, header=0)
    table_name = file.stem.lower()

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"{table_name} inserted")

conn.close()

print("All data inserted successfully!")