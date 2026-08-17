import streamlit as st
from utils.db import run_query

st.title("Company Profile")

company_query = """
SELECT company_name
FROM companies
ORDER BY company_name
"""
companies = run_query(company_query)

selected_company = st.selectbox(
    "Select Company",
    companies["company_name"]
)
if selected_company:

    profile_query = f"""
SELECT
    company_name,
    about_company,
    website,
    nse_profile,
    bse_profile,
    face_value,
    book_value,
    roe_percentage,
    roce_percentage
FROM companies
WHERE company_name = '{selected_company}'
"""

    profile = run_query(profile_query)

    if not profile.empty:
        row = profile.iloc[0]



        st.subheader(row["company_name"])

        st.write("**About:**", row["about_company"])
        st.write("**Website:**", row["website"])
        st.write("**NSE Profile:**", row["nse_profile"])
        st.write("**BSE Profile:**", row["bse_profile"])
        st.write("**Face Value:**", row["face_value"])
        st.write("**Book Value:**", row["book_value"])
        st.write("**ROE:**", row["roe_percentage"])
        st.write("**ROCE:**", row["roce_percentage"])

        st.subheader("Key Performance Indicators")

    kpi_query = f"""
    SELECT
        return_on_equity_pct AS roe,
        operating_profit_margin_pct AS roce,
        net_profit_margin_pct AS net_profit_margin,
        debt_to_equity AS debt_to_equity,
        free_cash_flow_cr AS fcf
    FROM financial_ratios fr
    JOIN companies c
         ON fr.company_id = c.id
    WHERE c.company_name = '{selected_company}'
    ORDER BY year DESC
    LIMIT 1
    """

    kpi = run_query(kpi_query)

    if not kpi.empty:
        r = kpi.iloc[0]

    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

    col1.metric("ROE", r["roe"])
    col2.metric("Operating Profit Margin", r["roce"])
    col3.metric("Net Profit Margin", r["net_profit_margin"])

    col4.metric("D/E", r["debt_to_equity"])
    col5.metric("FCF", r["fcf"])