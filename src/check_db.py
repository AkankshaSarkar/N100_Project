import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(sectors)")
print("SECTORS TABLE")
for row in cursor.fetchall():
    print(row)

print("\n")

cursor.execute("PRAGMA table_info(peer_groups)")
print("PEER_GROUPS TABLE")
for row in cursor.fetchall():
    print(row)

conn.close()