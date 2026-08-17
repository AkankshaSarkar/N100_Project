import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.utils.db import get_connection


st.title("Capital Analysis")
st.write("Analyze company market capitalization.")


# -----------------------------
# Database connection
# -----------------------------
conn = get_connection()


# -----------------------------
# Load latest market cap data
# -----------------------------
query = """
SELECT
    c.id AS company_id,
    c.company_name,
    s.broad_sector,
    mc.year,
    mc.market_cap_crore AS market_cap
FROM market_cap mc

JOIN companies c
    ON mc.company_id = c.id

LEFT JOIN sectors s
    ON s.company_id = c.id

WHERE mc.year = (
    SELECT MAX(mc2.year)
    FROM market_cap mc2
    WHERE mc2.company_id = mc.company_id
)

AND mc.market_cap_crore IS NOT NULL
"""

df = pd.read_sql_query(query, conn)

conn.close()


# -----------------------------
# Check data
# -----------------------------
if df.empty:
    st.warning("No market capitalization data available.")
    st.stop()


# -----------------------------
# Clean data
# -----------------------------
df["market_cap"] = pd.to_numeric(
    df["market_cap"],
    errors="coerce"
)

df = df.dropna(subset=["market_cap"])


# -----------------------------
# KPI Section
# -----------------------------
st.subheader("Market Capitalization KPIs")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Market Cap",
        f"₹{df['market_cap'].sum():,.0f} Cr"
    )

with col2:
    st.metric(
        "Median Market Cap",
        f"₹{df['market_cap'].median():,.0f} Cr"
    )

with col3:
    st.metric(
        "Companies",
        len(df)
    )


# -----------------------------
# Top Companies by Market Cap
# -----------------------------
st.subheader("Top Companies by Market Capitalization")

top_df = (
    df.sort_values(
        "market_cap",
        ascending=False
    )
    .head(15)
)

fig = px.bar(
    top_df,
    x="market_cap",
    y="company_name",
    orientation="h",
    title="Top 15 Companies by Market Cap",
    labels={
        "market_cap": "Market Cap (₹ Crore)",
        "company_name": "Company"
    }
)

fig.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------
# Sector-wise Market Cap
# -----------------------------
st.subheader("Sector-wise Market Capitalization")

sector_df = (
    df.dropna(subset=["broad_sector"])
    .groupby("broad_sector", as_index=False)["market_cap"]
    .sum()
    .sort_values(
        "market_cap",
        ascending=False
    )
)

fig_sector = px.bar(
    sector_df,
    x="broad_sector",
    y="market_cap",
    title="Market Cap by Sector",
    labels={
        "broad_sector": "Sector",
        "market_cap": "Market Cap (₹ Crore)"
    }
)

st.plotly_chart(
    fig_sector,
    use_container_width=True
)


# -----------------------------
# Market Cap Table
# -----------------------------
st.subheader("Company Market Capitalization")

display_df = df[
    [
        "company_name",
        "broad_sector",
        "year",
        "market_cap"
    ]
].sort_values(
    "market_cap",
    ascending=False
)

display_df["market_cap"] = display_df[
    "market_cap"
].round(2)

st.dataframe(
    display_df,
    use_container_width=True
)