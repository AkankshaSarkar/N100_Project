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
        "Sector Summary Report",
        "Cluster Profile Report"
    ]
)


# =========================================================
# COMPANY FINANCIAL REPORT
# =========================================================
if report_type == "Company Financial Report":

    st.subheader("Company Financial Report")

    query = """
    SELECT DISTINCT
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

        st.warning(
            "No financial report data available."
        )

    else:

        # Convert ROE to numeric
        df["roe"] = pd.to_numeric(
            df["roe"],
            errors="coerce"
        )

        # Remove rows where ROE is missing
        df = df.dropna(
            subset=["roe"]
        )

        # Number of companies
        st.metric(
            "Companies",
            len(df)
        )

        # Display report
        st.dataframe(
            df,
            width="stretch"
        )

        # CSV download
        csv_data = df.to_csv(
            index=False
        )

        st.download_button(
            label="Download Company Financial Report",
            data=csv_data,
            file_name="company_financial_report.csv",
            mime="text/csv"
        )


# =========================================================
# SECTOR SUMMARY REPORT
# =========================================================
elif report_type == "Sector Summary Report":

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

        st.warning(
            "No sector report data available."
        )

    else:

        # Convert average ROE to numeric
        sector_df["average_roe"] = pd.to_numeric(
            sector_df["average_roe"],
            errors="coerce"
        )

        # Round ROE
        sector_df["average_roe"] = (
            sector_df["average_roe"]
            .round(2)
        )

        # Display report
        st.dataframe(
            sector_df,
            width="stretch"
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


# =========================================================
# CLUSTER PROFILE REPORT
# =========================================================
elif report_type == "Cluster Profile Report":

    st.subheader("Cluster Profile Report")

    cluster_file = "output/cluster_profile.csv"

    try:

        cluster_df = pd.read_csv(
            cluster_file
        )

        if cluster_df.empty:

            st.warning(
                "No cluster profile data available."
            )

        else:

            # Number of clusters
            st.metric(
                "Clusters",
                len(cluster_df)
            )

            # Display cluster profile
            st.dataframe(
                cluster_df,
                width="stretch"
            )

            # CSV download
            csv_data = cluster_df.to_csv(
                index=False
            )

            st.download_button(
                label="Download Cluster Profile Report",
                data=csv_data,
                file_name="cluster_profile_report.csv",
                mime="text/csv"
            )

    except FileNotFoundError:

        st.error(
            "Cluster profile file not found. "
            "Please run cluster_profiling.py first."
        )

conn.close()