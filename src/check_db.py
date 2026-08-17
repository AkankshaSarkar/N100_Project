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

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("TABLES:")
for table in tables:
    print(table[0])    

print("\nFINANCIAL_RATIOS TABLE")

cursor.execute("PRAGMA table_info(financial_ratios)")
for row in cursor.fetchall():
    print(row)

print("\nMARKET_CAP TABLE")

cursor.execute("PRAGMA table_info(market_cap)")

for row in cursor.fetchall():
    print(row)

#cursor.execute("""
#SELECT year, COUNT(*)
#FROM market_cap
#GROUP BY year
#""")
#
#for row in cursor.fetchall():
#   print(row)

cursor.execute("PRAGMA table_info(companies)")

print("COMPANIES TABLE")

for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT * FROM companies LIMIT 5")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.execute("SELECT * FROM companies LIMIT 1")

row = cursor.fetchone()

print(len(row))

cursor.execute("PRAGMA table_info(financial_ratios)")

print("FINANCIAL_RATIOS COLUMNS")
for row in cursor.fetchall():
    print(row)

print("\nMARKET_CAP COLUMNS")

cursor.execute("PRAGMA table_info(market_cap)")
for row in cursor.fetchall():
    print(row)

print("\nFINANCIAL RATIOS YEARS")

cursor.execute("""
SELECT DISTINCT year
FROM financial_ratios
ORDER BY year
""")

for row in cursor.fetchall():
    print(row)


print("\nMARKET CAP YEARS")

cursor.execute("""
SELECT DISTINCT year
FROM market_cap
ORDER BY year
""")

for row in cursor.fetchall():
    print(row)

conn.close()