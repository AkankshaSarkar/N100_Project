import streamlit as st
from utils.db import run_query

st.title("🏠 Home")

# Year List

year_query = """
SELECT DISTINCT CAST(SUBSTR(year, 5, 4) AS INTEGER) AS year
FROM financial_ratios
WHERE year LIKE 'Dec %'
ORDER BY year
"""

years = run_query(year_query)

selected_year = st.sidebar.selectbox(
    "Select Year",
    years["year"].tolist()
)


# Total Companies

query = f"""
SELECT
    COUNT(DISTINCT fr.company_id) AS total_companies,
    ROUND(AVG(fr.return_on_equity_pct), 2) AS avg_roe,
    COALESCE(ROUND(AVG(mc.pe_ratio), 2), 0) AS avg_pe,
    COALESCE(ROUND(AVG(mc.pb_ratio), 2), 0) AS avg_pb,
    COALESCE(ROUND(AVG(fr.debt_to_equity), 2), 0) AS avg_de,
    SUM(CASE WHEN fr.debt_to_equity = 0 THEN 1 ELSE 0 END) AS debt_free_companies

FROM financial_ratios AS fr

LEFT JOIN market_cap AS mc
    ON fr.company_id = mc.company_id
    AND CAST(SUBSTR(fr."year", 5, 4) AS INTEGER) = mc."year"

WHERE fr."year" = 'Dec {selected_year}'
"""

df = run_query(query)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Companies",
        int(df["total_companies"].iloc[0])
    )

with col2:
    st.metric(
        "Average ROE",
        f"{df['avg_roe'].iloc[0]} %"
    )

with col3:
    st.metric(
        "Average P/E",
        df["avg_pe"].iloc[0]
    )


col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Average D/E",
        df["avg_de"].iloc[0]
    )

with col5:
    st.metric(
        "P/B Ratio",
        df["avg_pb"].iloc[0]
    )

with col6:
    st.metric(
        "Debt-Free Companies",
        int(df["debt_free_companies"].iloc[0])
    )