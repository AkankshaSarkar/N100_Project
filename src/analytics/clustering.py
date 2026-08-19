from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


FEATURES = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "asset_turnover",
    "free_cash_flow_cr",
]


def run_clustering():
    db_path = Path("db/nifty100.db")

    query = """
    SELECT
    c.id AS company_id,
    c.company_name,
    fr.year,
    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.operating_profit_margin_pct,
    fr.asset_turnover,
    fr.free_cash_flow_cr
FROM companies c
JOIN financial_ratios fr
    ON c.id = fr.company_id
    """

    import sqlite3

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convert year into a proper date
    df["year_date"] = pd.to_datetime(
        df["year"],
        format="%b %Y",
        errors="coerce"
    )

    # Keep latest available year for each company
    df = df.sort_values(["company_id", "year_date"])
    df = df.drop_duplicates(
        subset=["company_id"],
        keep="last"
    )

    # Impute missing values using overall median
    for feature in FEATURES:
        df[feature] = df[feature].fillna(df[feature].median())
    # Standardize features
    scaler = StandardScaler()
    X = scaler.fit_transform(df[FEATURES])

    # K-Means clustering
    kmeans = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10,
    )

    df["cluster_id"] = kmeans.fit_predict(X)

    # Distance from centroid
    distances = kmeans.transform(X)

    df["distance_from_centroid"] = [
        distances[i, cluster]
        for i, cluster in enumerate(df["cluster_id"])
    ]

    # Cluster names
    cluster_names = {
        0: "High-Quality Compounders",
        1: "Defensive Dividend Payers",
        2: "Value Cyclicals",
        3: "Distressed or Turnaround",
        4: "Emerging Growth",
    }

    df["cluster_name"] = df["cluster_id"].map(cluster_names)

    # Save cluster labels
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "cluster_labels.csv"

    df[
        [
            "company_id",
            "cluster_id",
            "cluster_name",
            "distance_from_centroid",
        ]
    ].to_csv(output_file, index=False)

    # Elbow plot
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    inertias = []

    for k in range(2, 11):
        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10,
        )
        model.fit(X)
        inertias.append(model.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(range(2, 11), inertias, marker="o")
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Inertia")
    plt.title("K-Means Elbow Plot")
    plt.xticks(range(2, 11))
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(reports_dir / "elbow_plot.png")
    plt.close()

    return df


if __name__ == "__main__":
    result = run_clustering()

    print(result["cluster_name"].value_counts())

    print("\nSaved: output/cluster_labels.csv")
    print("Saved: reports/elbow_plot.png")