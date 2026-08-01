import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("output/peer_percentile.csv")

print(df.head())
print(df.columns.tolist())


company = "ADANIGREEN"

metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "asset_turnover",
    "interest_coverage"
]

data = df[df["company_id"] == company].iloc[0]

values = [data[m] for m in metrics]
values += values[:1]

angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))

ax.plot(angles, values, linewidth=2)
ax.fill(angles, values, alpha=0.25)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(metrics)

plt.title(company)

plt.savefig("output/radar_chart.png")
plt.show()

print("Radar chart saved successfully!")