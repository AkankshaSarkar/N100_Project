from fastapi import FastAPI
import sqlite3

app = FastAPI(title="N100 Project API")
DB_PATH = "db/nifty100.db"

@app.get("/")
def home():
    return {
        "message": "N100 Project API is running successfully"
    }

@app.get("/health")
def health():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = [
        "companies",
        "financial_ratios",
        "market_cap",
        "peer_groups",
        "profitandloss",
        "prosandcons",
        "sectors",
        "stock_prices",
        "balancesheet",
        "cashflow",
    ]

    db_row_counts = {}

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        db_row_counts[table] = cursor.fetchone()[0]

    conn.close()

    return {
        "status": "ok",
        "db_row_counts": db_row_counts
    }


@app.get("/companies")
def get_companies():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, company_name, website, roe_percentage
        FROM companies
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

@app.get("/companies/{company_id}/ratios")
def get_company_ratios(company_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        year,
        net_profit_margin_pct,
        operating_profit_margin_pct,
        return_on_equity_pct,
        debt_to_equity,
        interest_coverage,
        asset_turnover,
        free_cash_flow_cr,
        capex_cr,
        earnings_per_share,
        book_value_per_share,
        dividend_payout_ratio_pct,
        total_debt_cr,
        cash_from_operations_cr
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year
""", (company_id,))    

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]