import streamlit as st
import pandas as pd

from dashboard.utils.db import get_connection


st.title("Reports")
st.write("Generate and download analytical reports from the Nifty 100 database.")


# --------------------------------
# Database connection
# --------------------------------
conn = get_connection()


# --------------------------------
# Report type
# --------------------------------
report_type = st.selectbox(
    "Select Report",
    [
        "Company Financial Report",
        "Sector Summary Report"
    ]
)


# =========================================================
# COMPANY FINANCIAL REPORT
# =========================================================
if report_type == "Company Financial Report":

    st.subheader("Company Financial Report")

    query = """
    SELECT
        c.id AS company_id,
        c.company_name,
        s.broad_sector,
        s.sub_sector,
        fr.year,
        fr.return_on_equity_pct AS roe
    FROM financial_ratios fr

    JOIN companies c
        ON fr.company_id = c.id

    LEFT JOIN sectors s
        ON s.company_id = c.id

    WHERE fr.year = (
        SELECT MAX(fr2.year)
        FROM financial_ratios fr2
        WHERE fr2.company_id = fr.company_id
    )

    AND fr.return_on_equity_pct IS NOT NULL
    """

    df = pd.read_sql_query(query, conn)

    if df.empty:
        st.warning("No financial report data available.")
    else:

        df["roe"] = pd.to_numeric(
            df["roe"],
            errors="coerce"
        )

        df = df.dropna(subset=["roe"])

        st.metric(
            "Companies",
            len(df)
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        # CSV download
        csv_data = df.to_csv(index=False)

        st.download_button(
            label="Download Company Financial Report",
            data=csv_data,
            file_name="company_financial_report.csv",
            mime="text/csv"
        )


# =========================================================
# SECTOR SUMMARY REPORT
# =========================================================
else:

    st.subheader("Sector Summary Report")

    query = """
    SELECT
        s.broad_sector,
        COUNT(DISTINCT c.id) AS companies,
        AVG(fr.return_on_equity_pct) AS average_roe
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

    AND fr.return_on_equity_pct IS NOT NULL

    GROUP BY s.broad_sector

    ORDER BY average_roe DESC
    """

    sector_df = pd.read_sql_query(
        query,
        conn
    )

    if sector_df.empty:
        st.warning("No sector report data available.")
    else:

        sector_df["average_roe"] = pd.to_numeric(
            sector_df["average_roe"],
            errors="coerce"
        )

        sector_df["average_roe"] = (
            sector_df["average_roe"].round(2)
        )

        st.dataframe(
            sector_df,
            use_container_width=True
        )

        # CSV download
        csv_data = sector_df.to_csv(
            index=False
        )

        st.download_button(
            label="Download Sector Summary Report",
            data=csv_data,
            file_name="sector_summary_report.csv",
            mime="text/csv"
        )
conn.close()