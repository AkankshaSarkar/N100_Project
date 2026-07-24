from pathlib import Path
import sqlite3
import pandas as pd
import yaml

CONFIG_PATH = Path("config/screener_config.yaml")
DB_PATH = Path("db/nifty100.db")

with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

conn = sqlite3.connect(DB_PATH)

query = """
SELECT *
FROM financial_ratios
"""

df = pd.read_sql_query(query, conn)
print(df.columns.tolist())
print(df.head())

preset_name = input(
    "Enter preset (quality/value/growth/income): "
).lower()

if preset_name not in config["presets"]:
    print("Invalid preset!")
    exit()

preset = config["presets"][preset_name]
print("Selected Preset:", preset_name)
print(preset)
print(config["presets"])

filtered_df = df[
    (df["return_on_equity_pct"] >= preset["roe_min"]) &
    (df["debt_to_equity"] <= preset["de_max"])
]

print(filtered_df.head())
print("Total rows:", len(df))
print("Filtered rows:", len(filtered_df))

filtered_df.to_csv("output/screener_output.csv", index=False)
print("Output saved successfully.")

conn.close()
exit()