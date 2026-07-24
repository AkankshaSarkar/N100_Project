import sqlite3
from pathlib import Path

DB_PATH = Path("db/nifty100.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

with open("sql/schema.sql", "r") as file:
    cursor.executescript(file.read())

conn.commit()

print("Tables created successfully!")

conn.close()