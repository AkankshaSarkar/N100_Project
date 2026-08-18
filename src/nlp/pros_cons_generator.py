import sqlite3
from pathlib import Path
import pandas as pd


# ============================================================
# PATHS
# ============================================================

DB_PATH = Path("db/nifty100.db")
PARSED_FILE = Path("output/analysis_parsed.csv")
OUTPUT_FILE = Path("output/pros_cons_generated.csv")


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return sqlite3.connect(DB_PATH)


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    conn = get_connection()

    companies = pd.read_sql_query(
        "SELECT * FROM companies",
        conn
    )

    financial = pd.read_sql_query(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    # Load parsed analysis file if available
    if PARSED_FILE.exists():

        parsed = pd.read_csv(PARSED_FILE)

    else:

        parsed = pd.DataFrame(
            columns=[
                "company_id",
                "metric_type",
                "period_years",
                "value_pct"
            ]
        )

    return companies, financial, parsed


# ============================================================
# COLUMN NORMALIZATION
# ============================================================

def normalize_financial_columns(financial):

    """
    Converts database column names into simple names used
    by the PRO/CON rules.
    """

    column_map = {}

    # ROE
    if "return_on_equity_pct" in financial.columns:
        column_map["return_on_equity_pct"] = "roe"

    elif "roe" in financial.columns:
        column_map["roe"] = "roe"

    # Operating profit margin
    if "operating_profit_margin_pct" in financial.columns:
        column_map["operating_profit_margin_pct"] = (
            "operating_profit_margin"
        )

    elif "operating_profit_margin" in financial.columns:
        column_map["operating_profit_margin"] = (
            "operating_profit_margin"
        )

    # Debt to equity
    if "debt_to_equity" in financial.columns:
        column_map["debt_to_equity"] = "debt_to_equity"

    # Interest coverage
    if "interest_coverage" in financial.columns:
        column_map["interest_coverage"] = "interest_coverage"

    # Free cash flow
    if "free_cash_flow_cr" in financial.columns:
        column_map["free_cash_flow_cr"] = "free_cash_flow"

    elif "free_cash_flow" in financial.columns:
        column_map["free_cash_flow"] = "free_cash_flow"

    # Asset turnover
    if "asset_turnover" in financial.columns:
        column_map["asset_turnover"] = "asset_turnover"

    # Dividend payout
    if "dividend_payout_ratio_pct" in financial.columns:
        column_map["dividend_payout_ratio_pct"] = (
            "dividend_payout"
        )

    elif "dividend_payout" in financial.columns:
        column_map["dividend_payout"] = "dividend_payout"

    # ROCE
    roce_candidates = [
        "return_on_capital_employed_pct",
        "return_on_capital_employed",
        "roce_pct",
        "roce"
    ]

    for col in roce_candidates:

        if col in financial.columns:

            column_map[col] = "roce"
            break

    financial = financial.rename(
        columns=column_map
    )

    return financial


# ============================================================
# GET LATEST FINANCIAL RECORD
# ============================================================

def get_latest(financial_company):

    if financial_company.empty:
        return None

    if "year" in financial_company.columns:

        financial_company = financial_company.sort_values(
            "year"
        )

    return financial_company.iloc[-1]


# ============================================================
# GET PARSED VALUE
# ============================================================

def get_parsed_value(
    parsed,
    company_id,
    metric,
    years
):

    if parsed.empty:
        return None

    required_columns = [
        "company_id",
        "metric_type",
        "period_years",
        "value_pct"
    ]

    for col in required_columns:

        if col not in parsed.columns:
            return None

    data = parsed[
        (parsed["company_id"] == company_id)
        &
        (parsed["metric_type"] == metric)
        &
        (parsed["period_years"] == years)
    ]

    if data.empty:
        return None

    try:

        return float(
            data.iloc[0]["value_pct"]
        )

    except (ValueError, TypeError):

        return None


# ============================================================
# CONFIDENCE
# ============================================================

def confidence_from_strength(
    value,
    threshold
):

    if value is None:
        return 0.0

    if threshold == 0:
        return 60.0

    strength = abs(value) / abs(threshold)

    confidence = 60 + min(
        strength * 20,
        40
    )

    return round(
        confidence,
        2
    )


# ============================================================
# PRO RULES
# ============================================================

def generate_pros(
    company_id,
    row,
    parsed,
    company_financial
):

    pros = []

    # --------------------------------------------------------
    # PRO 01
    # ROE > 20%
    # --------------------------------------------------------

    roe = row.get("roe")

    if pd.notna(roe) and roe > 20:

        pros.append({
            "type": "pro",
            "rule_id": "PRO_01",
            "text": (
                "Consistently high return on equity above 20% "
                "demonstrates exceptional capital efficiency"
            ),
            "confidence_pct": confidence_from_strength(
                roe,
                20
            )
        })

    # --------------------------------------------------------
    # PRO 02
    # Positive FCF
    # --------------------------------------------------------

    fcf = row.get("free_cash_flow")

    if pd.notna(fcf) and fcf > 0:

        pros.append({
            "type": "pro",
            "rule_id": "PRO_02",
            "text": (
                "Positive free cash flow indicates "
                "healthy cash generation"
            ),
            "confidence_pct": 80.0
        })

    # --------------------------------------------------------
    # PRO 03
    # Debt to Equity = 0
    # --------------------------------------------------------

    de = row.get("debt_to_equity")

    if pd.notna(de) and de == 0:

        pros.append({
            "type": "pro",
            "rule_id": "PRO_03",
            "text": (
                "Debt-free balance sheet provides "
                "financial flexibility and eliminates "
                "interest burden"
            ),
            "confidence_pct": 95.0
        })

    # --------------------------------------------------------
    # PRO 04
    # Revenue CAGR > 15%
    # --------------------------------------------------------

    revenue_cagr = get_parsed_value(
        parsed,
        company_id,
        "compounded_sales_growth",
        5
    )

    if (
        revenue_cagr is not None
        and revenue_cagr > 15
    ):

        pros.append({
            "type": "pro",
            "rule_id": "PRO_04",
            "text": (
                "Revenue growing at above 15% CAGR over "
                "5 years reflects strong business momentum"
            ),
            "confidence_pct": confidence_from_strength(
                revenue_cagr,
                15
            )
        })

    # --------------------------------------------------------
    # PRO 05
    # Operating Profit Margin > 25%
    # --------------------------------------------------------

    opm = row.get(
        "operating_profit_margin"
    )

    if pd.notna(opm) and opm > 25:

        pros.append({
            "type": "pro",
            "rule_id": "PRO_05",
            "text": (
                "Operating profit margin above 25% indicates "
                "strong pricing power and cost discipline"
            ),
            "confidence_pct": confidence_from_strength(
                opm,
                25
            )
        })

    # --------------------------------------------------------
    # PRO 06
    # PAT CAGR > 20%
    # --------------------------------------------------------

    pat_cagr = get_parsed_value(
        parsed,
        company_id,
        "compounded_profit_growth",
        5
    )

    if (
        pat_cagr is not None
        and pat_cagr > 20
    ):

        pros.append({
            "type": "pro",
            "rule_id": "PRO_06",
            "text": (
                "Net profit compounding above 20% over "
                "5 years creates significant shareholder value"
            ),
            "confidence_pct": confidence_from_strength(
                pat_cagr,
                20
            )
        })

    # --------------------------------------------------------
    # PRO 07
    # ICR > 10 OR Debt Free
    # --------------------------------------------------------

    icr = row.get(
        "interest_coverage"
    )

    if (
        (
            pd.notna(icr)
            and icr > 10
        )
        or
        (
            pd.notna(de)
            and de == 0
        )
    ):

        pros.append({
            "type": "pro",
            "rule_id": "PRO_07",
            "text": (
                "Very high interest coverage or debt-free "
                "position reflects negligible financial stress"
            ),
            "confidence_pct": 90.0
        })

    # --------------------------------------------------------
    # PRO 08
    # Dividend Yield > 2% + Positive FCF
    # --------------------------------------------------------

    dividend_yield = row.get(
        "dividend_yield"
    )

    if (
        pd.notna(dividend_yield)
        and dividend_yield > 2
        and pd.notna(fcf)
        and fcf > 0
    ):

        pros.append({
            "type": "pro",
            "rule_id": "PRO_08",
            "text": (
                "Consistent dividend yield above 2% backed "
                "by positive free cash flow"
            ),
            "confidence_pct": 85.0
        })

    # --------------------------------------------------------
    # PRO 09
    # EPS CAGR > 15%
    # --------------------------------------------------------

    eps_cagr = get_parsed_value(
        parsed,
        company_id,
        "eps_growth",
        5
    )

    if (
        eps_cagr is not None
        and eps_cagr > 15
    ):

        pros.append({
            "type": "pro",
            "rule_id": "PRO_09",
            "text": (
                "Earnings per share growing above 15% CAGR "
                "indicates strong earnings quality and compounding"
            ),
            "confidence_pct": confidence_from_strength(
                eps_cagr,
                15
            )
        })

    # --------------------------------------------------------
    # PRO 10
    # ROE improving for 3 consecutive years
    # --------------------------------------------------------

    roe_improving = False

    if (
        company_financial is not None
        and not company_financial.empty
    ):

        roe_history = company_financial.copy()

        if (
            "year" in roe_history.columns
            and "roe" in roe_history.columns
        ):

            roe_history["year_dt"] = pd.to_datetime(
                roe_history["year"],
                errors="coerce"
            )

            roe_history = (
                roe_history
                .dropna(
                    subset=[
                        "year_dt",
                        "roe"
                    ]
                )
                .sort_values("year_dt")
            )

            if len(roe_history) >= 3:

                last_three = (
                    roe_history
                    .tail(3)["roe"]
                    .tolist()
                )

                if (
                    last_three[0] < last_three[1]
                    and last_three[1] < last_three[2]
                ):

                    roe_improving = True

    if roe_improving:

        pros.append({
            "type": "pro",
            "rule_id": "PRO_10",
            "text": (
                "Return on equity improving for 3 consecutive "
                "years shows strengthening business quality"
            ),
            "confidence_pct": 85.0
        })

    # --------------------------------------------------------
    # PRO 11
    # Revenue CAGR > PAT CAGR
    # --------------------------------------------------------

    if (
        revenue_cagr is not None
        and pat_cagr is not None
        and revenue_cagr > pat_cagr
    ):

        pros.append({
            "type": "pro",
            "rule_id": "PRO_11",
            "text": (
                "Revenue growth exceeding profit growth "
                "shows strong business expansion"
            ),
            "confidence_pct": 70.0
        })

    # --------------------------------------------------------
    # PRO 12
    # Asset Turnover > 1
    # --------------------------------------------------------

    asset_turnover = row.get(
        "asset_turnover"
    )

    if (
        pd.notna(asset_turnover)
        and asset_turnover > 1
    ):

        pros.append({
            "type": "pro",
            "rule_id": "PRO_12",
            "text": (
                "Asset turnover above 1 indicates "
                "efficient utilization of the asset base"
            ),
            "confidence_pct": 75.0
        })

    return pros


# ============================================================
# CON RULES
# ============================================================

def generate_cons(
    company_id,
    row,
    parsed,
    company_financial
):

    cons = []

    de = row.get(
        "debt_to_equity"
    )

    icr = row.get(
        "interest_coverage"
    )

    opm = row.get(
        "operating_profit_margin"
    )

    roe = row.get(
        "roe"
    )

    roce = row.get(
        "roce"
    )

    fcf = row.get(
        "free_cash_flow"
    )

    dividend_payout = row.get(
        "dividend_payout"
    )

    revenue_cagr = get_parsed_value(
        parsed,
        company_id,
        "compounded_sales_growth",
        5
    )

    # --------------------------------------------------------
    # CON 01
    # D/E > 2
    # --------------------------------------------------------

    if pd.notna(de) and de > 2:

        cons.append({
            "type": "con",
            "rule_id": "CON_01",
            "text": (
                "High debt-to-equity ratio indicates elevated "
                "financial leverage and warrants monitoring"
            ),
            "confidence_pct": confidence_from_strength(
                de,
                2
            )
        })

    # --------------------------------------------------------
    # CON 02
    # Negative FCF
    # --------------------------------------------------------

    if pd.notna(fcf) and fcf < 0:

        cons.append({
            "type": "con",
            "rule_id": "CON_02",
            "text": (
                "Negative free cash flow raises concern "
                "about cash generation quality"
            ),
            "confidence_pct": 85.0
        })

    # --------------------------------------------------------
    # CON 03
    # OPM < 10%
    # --------------------------------------------------------

    if pd.notna(opm) and opm < 10:

        cons.append({
            "type": "con",
            "rule_id": "CON_03",
            "text": (
                "Low operating profit margin suggests "
                "pricing pressure or high operating costs"
            ),
            "confidence_pct": 80.0
        })

    # --------------------------------------------------------
    # CON 04
    # Negative ROE
    # --------------------------------------------------------

    if pd.notna(roe) and roe < 0:

        cons.append({
            "type": "con",
            "rule_id": "CON_04",
            "text": (
                "Negative return on equity indicates "
                "poor shareholder returns"
            ),
            "confidence_pct": 90.0
        })

    # --------------------------------------------------------
    # CON 05
    # Revenue CAGR < 5%
    # --------------------------------------------------------

    if (
        revenue_cagr is not None
        and revenue_cagr < 5
    ):

        cons.append({
            "type": "con",
            "rule_id": "CON_05",
            "text": (
                "Revenue growing below 5% over 5 years "
                "suggests limited business momentum"
            ),
            "confidence_pct": 80.0
        })

    # --------------------------------------------------------
    # CON 06
    # ICR < 1.5
    # --------------------------------------------------------

    if pd.notna(icr) and icr < 1.5:

        cons.append({
            "type": "con",
            "rule_id": "CON_06",
            "text": (
                "Interest coverage below 1.5x indicates "
                "risk of difficulty meeting debt obligations"
            ),
            "confidence_pct": 90.0
        })

    # --------------------------------------------------------
    # CON 07
    # Dividend payout > 100%
    # --------------------------------------------------------

    if (
        pd.notna(dividend_payout)
        and dividend_payout > 100
    ):

        cons.append({
            "type": "con",
            "rule_id": "CON_07",
            "text": (
                "Dividend payout above 100% may indicate "
                "unsustainable distribution"
            ),
            "confidence_pct": 90.0
        })

    # --------------------------------------------------------
    # CON 08
    # D/E > 1
    # --------------------------------------------------------

    if pd.notna(de) and de > 1:

        cons.append({
            "type": "con",
            "rule_id": "CON_08",
            "text": (
                "Elevated debt-to-equity indicates "
                "higher financial leverage"
            ),
            "confidence_pct": 70.0
        })

    # --------------------------------------------------------
    # CON 09
    # ROE < 10%
    # --------------------------------------------------------

    if pd.notna(roe) and roe < 10:

        cons.append({
            "type": "con",
            "rule_id": "CON_09",
            "text": (
                "Low return on equity indicates "
                "weak shareholder capital efficiency"
            ),
            "confidence_pct": 75.0
        })

    # --------------------------------------------------------
    # CON 10
    # ROCE < 10%
    # --------------------------------------------------------

    if pd.notna(roce) and roce < 10:

        cons.append({
            "type": "con",
            "rule_id": "CON_10",
            "text": (
                "ROCE below 10% suggests insufficient "
                "returns on invested capital"
            ),
            "confidence_pct": 80.0
        })

    # --------------------------------------------------------
    # CON 11
    # Asset turnover < 0.5
    # --------------------------------------------------------

    asset_turnover = row.get(
        "asset_turnover"
    )

    if (
        pd.notna(asset_turnover)
        and asset_turnover < 0.5
    ):

        cons.append({
            "type": "con",
            "rule_id": "CON_11",
            "text": (
                "Low asset turnover suggests inefficient "
                "utilization of the asset base"
            ),
            "confidence_pct": 75.0
        })

    # --------------------------------------------------------
    # CON 12
    # Revenue CAGR < 5%
    # --------------------------------------------------------

    if (
        revenue_cagr is not None
        and revenue_cagr < 5
    ):

        cons.append({
            "type": "con",
            "rule_id": "CON_12",
            "text": (
                "Weak revenue growth indicates "
                "limited business momentum"
            ),
            "confidence_pct": 75.0
        })

    return cons


# ============================================================
# MAIN GENERATOR
# ============================================================

def generate_pros_cons():

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    companies, financial, parsed = load_data()

    # Normalize DB column names
    financial = normalize_financial_columns(
        financial
    )

    results = []

    # --------------------------------------------------------
    # PROCESS EVERY COMPANY
    # --------------------------------------------------------

    for _, company in companies.iterrows():

        company_id = company["id"]

        company_financial = financial[
            financial["company_id"] == company_id
        ]

        row = get_latest(
            company_financial
        )

        if row is None:
            continue

        # Generate PROS
        pros = generate_pros(
            company_id,
            row,
            parsed,
            company_financial
        )

        # Generate CONS
        cons = generate_cons(
            company_id,
            row,
            parsed,
            company_financial
        )

        # ----------------------------------------------------
        # VALID PROS
        # ----------------------------------------------------

        valid_pros = [
            item
            for item in pros
            if item["confidence_pct"] > 60
        ]

        # ----------------------------------------------------
        # VALID CONS
        # ----------------------------------------------------

        valid_cons = [
            item
            for item in cons
            if item["confidence_pct"] > 60
        ]

        # ----------------------------------------------------
        # FALLBACK PRO
        # ----------------------------------------------------

        if not valid_pros:

            fallback_pro = None

            # Positive ROE
            if (
                pd.notna(row.get("roe"))
                and row.get("roe") > 0
            ):

                fallback_pro = {
                    "type": "pro",
                    "rule_id": "PRO_01",
                    "text": (
                        "Positive return on equity indicates "
                        "the company is generating returns "
                        "on shareholder capital"
                    ),
                    "confidence_pct": 65.0
                }

            # Positive operating margin
            elif (
                pd.notna(
                    row.get(
                        "operating_profit_margin"
                    )
                )
                and row.get(
                    "operating_profit_margin"
                ) > 0
            ):

                fallback_pro = {
                    "type": "pro",
                    "rule_id": "PRO_05",
                    "text": (
                        "Positive operating profit margin "
                        "indicates the company generates "
                        "operating profit"
                    ),
                    "confidence_pct": 65.0
                }

            # Positive asset turnover
            elif (
                pd.notna(
                    row.get("asset_turnover")
                )
                and row.get(
                    "asset_turnover"
                ) > 0
            ):

                fallback_pro = {
                    "type": "pro",
                    "rule_id": "PRO_12",
                    "text": (
                        "Positive asset turnover indicates "
                        "the company is utilizing its asset base"
                    ),
                    "confidence_pct": 65.0
                }

            if fallback_pro is not None:

                valid_pros.append(
                    fallback_pro
                )

        # ----------------------------------------------------
        # FALLBACK CON
        # ----------------------------------------------------

        if not valid_cons:

            fallback_con = None

            # ROE below 15%
            if (
                pd.notna(row.get("roe"))
                and row.get("roe") < 15
            ):

                fallback_con = {
                    "type": "con",
                    "rule_id": "CON_09",
                    "text": (
                        "Return on equity below 15% indicates "
                        "relatively weak shareholder capital efficiency"
                    ),
                    "confidence_pct": 65.0
                }

            # Operating margin below 25%
            elif (
                pd.notna(
                    row.get(
                        "operating_profit_margin"
                    )
                )
                and row.get(
                    "operating_profit_margin"
                ) < 25
            ):

                fallback_con = {
                    "type": "con",
                    "rule_id": "CON_03",
                    "text": (
                        "Operating profit margin below 25% "
                        "indicates room for improvement "
                        "in operating efficiency"
                    ),
                    "confidence_pct": 65.0
                }

            # Debt-to-equity above 0
            elif (
                pd.notna(
                    row.get("debt_to_equity")
                )
                and row.get(
                    "debt_to_equity"
                ) > 0
            ):

                fallback_con = {
                    "type": "con",
                    "rule_id": "CON_08",
                    "text": (
                        "Presence of debt-to-equity indicates "
                        "some degree of financial leverage"
                    ),
                    "confidence_pct": 65.0
                }

            if fallback_con is not None:

                valid_cons.append(
                    fallback_con
                )

        # ----------------------------------------------------
        # SAVE PRO + CON RECORDS
        # ----------------------------------------------------

        for item in valid_pros + valid_cons:

            results.append({
                "company_id": company_id,
                "type": item["type"],
                "rule_id": item["rule_id"],
                "text": item["text"],
                "confidence_pct": item["confidence_pct"]
            })

    # ========================================================
    # CREATE OUTPUT DATAFRAME
    # ========================================================

    output_df = pd.DataFrame(
        results,
        columns=[
            "company_id",
            "type",
            "rule_id",
            "text",
            "confidence_pct"
        ]
    )

    # ========================================================
    # SAVE CSV
    # ========================================================

    output_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    print("======================================")
    print("PROS / CONS GENERATOR COMPLETE")
    print("======================================")

    print(
        f"Companies       : "
        f"{companies['id'].nunique()}"
    )

    print(
        f"Generated rows  : "
        f"{len(output_df)}"
    )

    print(
        f"Pro records     : "
        f"{(output_df['type'] == 'pro').sum()}"
    )

    print(
        f"Con records     : "
        f"{(output_df['type'] == 'con').sum()}"
    )

    print(
        f"Saved           : "
        f"{OUTPUT_FILE}"
    )

    print("\nFirst 10 records:")

    if not output_df.empty:

        print(
            output_df
            .head(10)
            .to_string(index=False)
        )

    else:

        print("No PRO/CON records generated.")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    generate_pros_cons()