import streamlit as st
import pandas as pd
from utils.db import run_query

st.title("Peer Comparison")

st.write("Compare a company with other companies from the same sector.")

# --------------------------------------------------
# Company List
# --------------------------------------------------

company_query = """
SELECT
    c.id,
    c.company_name,
    s.broad_sector
FROM companies c
LEFT JOIN sectors s
    ON s.company_id = c.id
WHERE c.company_name IS NOT NULL
ORDER BY c.company_name
"""

companies_df = run_query(company_query)

if companies_df.empty:
    st.warning("No companies found in database.")
    st.stop()

# --------------------------------------------------
# Company Selection
# --------------------------------------------------

selected_company = st.selectbox(
    "Select Company",
    companies_df["company_name"].tolist()
)

selected_row = companies_df[
    companies_df["company_name"] == selected_company
].iloc[0]

company_id = selected_row["id"]
sector = selected_row["broad_sector"]

st.write(f"**Sector:** {sector}")

# --------------------------------------------------
# Peer Comparison Query
# --------------------------------------------------

peer_query = f"""
SELECT
    c.company_name,
    s.broad_sector AS sector,
    fr.year,
    fr.return_on_equity_pct AS roe,
    fr.operating_profit_margin_pct AS operating_profit_margin,
    fr.net_profit_margin_pct AS net_profit_margin,
    fr.debt_to_equity AS debt_to_equity,
    fr.free_cash_flow_cr AS free_cash_flow,
    fr.earnings_per_share AS eps
FROM financial_ratios fr
JOIN companies c
    ON fr.company_id = c.id
JOIN sectors s
    ON s.company_id = c.id
WHERE s.broad_sector = '{sector}'
AND fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
ORDER BY fr.return_on_equity_pct DESC
"""

peers_df = run_query(peer_query)

# --------------------------------------------------
# Display Results
# --------------------------------------------------

if peers_df.empty:
    st.warning("No peer companies found.")
    st.stop()

st.subheader("Peer Companies")

st.dataframe(
    peers_df,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# Selected Company Performance
# --------------------------------------------------

st.subheader("Selected Company Performance")

selected_data = peers_df[
    peers_df["company_name"] == selected_company
]

if not selected_data.empty:

    row = selected_data.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "ROE (%)",
            round(row["roe"], 2)
        )

    with col2:
        st.metric(
            "Operating Margin (%)",
            round(row["operating_profit_margin"], 2)
        )

    with col3:
        st.metric(
            "Net Profit Margin (%)",
            round(row["net_profit_margin"], 2)
        )

    with col4:
        st.metric(
            "Debt-to-Equity",
            round(row["debt_to_equity"], 2)
        )

# --------------------------------------------------
# ROE Ranking
# --------------------------------------------------

st.subheader("ROE Ranking")

ranking_df = peers_df[
    ["company_name", "roe", "net_profit_margin", "debt_to_equity"]
].copy()

ranking_df = ranking_df.sort_values(
    "roe",
    ascending=False
).reset_index(drop=True)

ranking_df.insert(
    0,
    "Rank",
    ranking_df.index + 1
)

st.dataframe(
    ranking_df,
    use_container_width=True,
    hide_index=True
)