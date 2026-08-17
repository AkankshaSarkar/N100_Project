import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.utils.db import get_connection


st.title("Sector Analysis")
st.write("Analyze companies within a selected sector.")


# -----------------------------
# Load sectors
# -----------------------------
conn = get_connection()

sector_query = """
SELECT DISTINCT broad_sector
FROM sectors
WHERE broad_sector IS NOT NULL
ORDER BY broad_sector
"""

sectors_df = pd.read_sql_query(sector_query, conn)

sector_list = sectors_df["broad_sector"].dropna().tolist()

selected_sector = st.selectbox(
    "Select Sector",
    sector_list
)


# -----------------------------
# Load company financial data
# -----------------------------
query = """
SELECT
    c.id AS company_id,
    c.company_name,
    s.broad_sector,
    s.sub_sector,
    fr.year,
    fr.return_on_equity_pct AS roe,
    mc.market_cap_crore AS market_cap
FROM financial_ratios fr

JOIN companies c
    ON fr.company_id = c.id

JOIN sectors s
    ON s.company_id = c.id


LEFT JOIN market_cap mc
    ON mc.company_id = c.id
    AND mc.year = fr.year

WHERE s.broad_sector = ?

AND fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
"""
df = pd.read_sql_query(
    query,
    conn,
    params=(selected_sector,)
)

conn.close()


# -----------------------------
# Check data
# -----------------------------
if df.empty:
    st.warning("No data available for this sector.")
    st.stop()


# -----------------------------
# Clean numeric columns
# -----------------------------
for col in ["roe","market_cap"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["roe"])
# Market cap cannot be NaN or negative for bubble size
if df["market_cap"].notna().any():
    median_market_cap = df["market_cap"].dropna().median()

    df["market_cap"] = df["market_cap"].fillna(median_market_cap)
    df["market_cap"] = df["market_cap"].clip(lower=0)
else:
    # If no market-cap data exists
    df["market_cap"] = 1

# -----------------------------
# Bubble Chart
# -----------------------------
st.subheader(f"{selected_sector} — Company Analysis")

fig = px.scatter(
    df,
    x="roe",
    y="company_name",
    size="market_cap",
    hover_data=[
        "company_name",
        "broad_sector",
        "sub_sector",
        "year",
        "roe",
        "market_cap"
    ],
    title="ROE vs Company"
)
fig.update_traces(
    marker=dict(
        sizemin=8,
        opacity=0.75
    )
)

fig.update_layout(
    xaxis_title="ROE (%)",
    yaxis_title="Company",
    height=max(500, len(df) * 35),
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# -----------------------------
# Sector Median KPIs
# -----------------------------
st.subheader("Sector Median KPIs")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Median ROE",
        f"{df['roe'].median():.2f}%"
    )

with col2:
    st.metric(
        "Companies",
        len(df)
    )


# -----------------------------
# Sector Median Chart
# -----------------------------
median_roe = df["roe"].median()

median_chart_df = pd.DataFrame({
    "Metric": ["Median ROE"],
    "Value": [median_roe]
})


fig_med = px.bar(
    median_chart_df,
    x="Metric",
    y="Value",
   text="Value",
    title="Sector Median"
)

fig_med.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_med.update_layout(
    yaxis_title="ROE (%)",
    xaxis_title="",
    yaxis_range=[0, median_roe * 1.25],
    height=400
)

st.plotly_chart(
    fig_med,
    use_container_width=True
)