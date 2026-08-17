import pandas as pd
from pathlib import Path
from normaliser import normalize_ticker, normalize_year

DATA_PATH = Path("Data/raw")

excel_files = list(DATA_PATH.glob("*.xlsx"))

print(f"Total files found: {len(excel_files)}\n")

datasets = {}

for file in excel_files:
    
    df = pd.read_excel(file, header=1)
    df = normalize_ticker(df)
    df = normalize_year(df)
    datasets[file.stem] = df
    print(f"{file.name} --> {df.shape}")

print("\nColumn Names:\n")

for name, df in datasets.items():
    print(f"{name}:")
    print(df.columns.tolist())
    print("-" * 50)


print("\nAll datasets loaded successfully!")

analysis = pd.read_excel("Data/raw/analysis.xlsx", header=None)
print(analysis.head(10))

balancesheet = pd.read_excel("Data/raw/balancesheet.xlsx", header=None)
print(balancesheet.head(10))

cashflow = pd.read_excel("Data/raw/cashflow.xlsx", header=None)
print(cashflow.head(10))


df = pd.read_excel("Data/raw/companies.xlsx", header=None)
print(df.head(10))