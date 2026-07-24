CREATE TABLE IF NOT EXISTS companies (
    id TEXT PRIMARY KEY,
    company_name TEXT,
    sector TEXT,
    roe_percentage REAL
);

CREATE TABLE IF NOT EXISTS financial_ratios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT,
    year INTEGER,

    net_profit_margin REAL,
    operating_profit_margin REAL,
    roe REAL,
    roce REAL,
    roa REAL,

    debt_to_equity REAL,
    interest_coverage REAL,
    asset_turnover REAL,

    free_cash_flow REAL,
    cfo_quality REAL,
    capex_intensity REAL,
    fcf_conversion REAL,

    FOREIGN KEY (company_id) REFERENCES companies(id)
);