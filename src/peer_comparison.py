import pandas as pd

df = pd.read_csv("output/peer_percentile.csv")

print(df.head())
print(df.columns.tolist())

output_file = "output/peer_comparison.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for group in df["peer_group_name"].dropna().unique():
        group_df = df[df["peer_group_name"] == group]

        sheet_name = group[:31]  # Excel sheet name max 31 chars
        group_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Excel report saved successfully: {output_file}")