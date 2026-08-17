import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from dashboard.utils.db import get_connection


st.title("Trend Analysis")
st.write("Analyze historical financial trends for a selected company.")


# ---------------------------------------------------------
# Load companies
# ---------------------------------------------------------
conn = get_connection()

company_query = """
SELECT
    c.id,
    c.company_name
FROM companies c
WHERE c.company_name IS NOT NULL
ORDER BY c.company_name
"""

companies_df = pd.read_sql_query(company_query, conn)


if companies_df.empty:
    st.warning("No companies available.")
    conn.close()
    st.stop()


# ---------------------------------------------------------
# Company Search
# ---------------------------------------------------------
search_text = st.text_input(
    "Search Company",
    placeholder="Type company name..."
)


if search_text:
    filtered_companies = companies_df[
        companies_df["company_name"]
        .str.contains(search_text, case=False, na=False)
    ]
else:
    filtered_companies = companies_df


if filtered_companies.empty:
    st.warning("No matching company found.")
    conn.close()
    st.stop()


selected_company_name = st.selectbox(
    "Select Company",
    filtered_companies["company_name"].tolist()
)


selected_company_id = filtered_companies.loc[
    filtered_companies["company_name"] == selected_company_name,
    "id"
].iloc[0]


# ---------------------------------------------------------
# Metric selection
# ---------------------------------------------------------
metric_options = {
    "ROE (%)": "return_on_equity_pct",
    "Operating Profit Margin (%)": "operating_profit_margin_pct",
    "Net Profit Margin (%)": "net_profit_margin_pct",
    "Debt-to-Equity": "debt_to_equity",
    "Free Cash Flow (₹ Cr)": "free_cash_flow_cr"
}


selected_metrics = st.multiselect(
    "Select Metrics (maximum 3)",
    options=list(metric_options.keys()),
    default=["ROE (%)"],
    max_selections=3
)


if not selected_metrics:
    st.info("Please select at least one metric.")
    conn.close()
    st.stop()


# ---------------------------------------------------------
# Trend Query
# ---------------------------------------------------------
selected_columns = ", ".join(
    [
        f"fr.{metric_options[metric]} AS metric_{i}"
        for i, metric in enumerate(selected_metrics)
    ]
)

trend_query = f"""
SELECT
    fr.year,
    {selected_columns}
FROM financial_ratios fr
WHERE fr.company_id = ?
ORDER BY CAST(substr(fr.year, -4) AS INTEGER) DESC
LIMIT 10
"""


trend_df = pd.read_sql_query(
    trend_query,
    conn,
    params=(selected_company_id,)
)

conn.close()


if trend_df.empty:
    st.warning(
        f"No trend data available for {selected_company_name}."
    )
    st.stop()


# ---------------------------------------------------------
# Sort oldest → newest
# ---------------------------------------------------------
trend_df["year_num"] = pd.to_numeric(
    trend_df["year"].astype(str).str[-4:],
    errors="coerce"
)

trend_df = trend_df.sort_values("year_num").reset_index(drop=True)


# ---------------------------------------------------------
# Chart
# ---------------------------------------------------------
fig = go.Figure()


for i, metric in enumerate(selected_metrics):

    column_name = f"metric_{i}"

    values = pd.to_numeric(
        trend_df[column_name],
        errors="coerce"
    )

    # Calculate YoY %
    yoy = values.pct_change() * 100

    fig.add_trace(
        go.Scatter(
            x=trend_df["year"],
            y=values,
            mode="lines+markers",
            name=metric,
            hovertemplate=(
                "<b>%{x}</b><br>"
                + metric
                + ": %{y:.2f}<extra></extra>"
            )
        )
    )

    # -----------------------------------------------------
    # YoY annotations
    # -----------------------------------------------------
    for j in range(1, len(trend_df)):

        if pd.isna(values.iloc[j]):
            continue

        if pd.isna(yoy.iloc[j]):
            continue

        fig.add_annotation(
            x=trend_df["year"].iloc[j],
            y=values.iloc[j],
            text=f"{yoy.iloc[j]:+.1f}%",
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-25,
            font=dict(size=10)
        )


# ---------------------------------------------------------
# Layout
# ---------------------------------------------------------
fig.update_layout(
    title=f"10-Year Financial Trend — {selected_company_name}",
    xaxis_title="Year",
    yaxis_title="Value",
    hovermode="x unified",
    height=600,
    margin=dict(l=60, r=30, t=80, b=60),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    )
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------------
# Data table
# ---------------------------------------------------------
st.subheader("Historical Data")

display_df = trend_df.copy()

display_df = display_df.drop(
    columns=["year_num"]
)

rename_columns = {
    "year": "Year"
}

for i, metric in enumerate(selected_metrics):
    rename_columns[f"metric_{i}"] = metric

display_df = display_df.rename(
    columns=rename_columns
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)