import streamlit as st
import pandas as pd
from utils.db import run_query

st.title("Stock Screener")

st.write("Filter Nifty 100 companies based on financial performance.")

# Load sectors
sector_query = """
SELECT DISTINCT broad_sector AS sector
FROM sectors
WHERE broad_sector IS NOT NULL
ORDER BY broad_sector
"""

sector_df = run_query(sector_query)

sectors = ["All"] + sector_df["sector"].dropna().tolist()

# Filters
col1, col2, col3 = st.columns(3)

with col1:
    selected_sector = st.selectbox(
        "Sector",
        sectors
    )

with col2:
    min_roe = st.number_input(
        "Minimum ROE (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )

with col3:
    max_de = st.number_input(
        "Maximum Debt-to-Equity",
        min_value=0.0,
        max_value=20.0,
        value=20.0,
        step=0.1
    )

min_net_margin = st.number_input(
    "Minimum Net Profit Margin (%)",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=1.0
)

# Screener Query
screener_query = f"""
SELECT
    c.company_name,
    s.broad_sector AS sector,
    fr.year,
    fr.return_on_equity_pct AS roe,
    fr.operating_profit_margin_pct AS operating_profit_margin,
    fr.net_profit_margin_pct AS net_profit_margin,
    fr.debt_to_equity AS debt_to_equity,
    fr.free_cash_flow_cr AS free_cash_flow
FROM financial_ratios fr
JOIN companies c
    ON fr.company_id = c.id
JOIN sectors s
    ON s.company_id = c.id
WHERE fr.year = (
    SELECT MAX(fr2.year)
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
AND fr.return_on_equity_pct >= {min_roe}
AND fr.debt_to_equity <= {max_de}
AND fr.net_profit_margin_pct >= {min_net_margin}
"""

# Add sector filter
if selected_sector != "All":
    screener_query += f"""
    AND s.broad_sector = '{selected_sector}'
"""

screener_query += """
ORDER BY fr.return_on_equity_pct DESC
"""
# Run Query
results = run_query(screener_query)

# Display Results
st.subheader("Screened Companies")

if results.empty:
    st.warning("No companies match the selected filters.")
else:
    st.success(f"{len(results)} companies found.")

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True
    )