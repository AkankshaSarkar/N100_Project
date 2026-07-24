-- Total cnumber of ompanies
SELECT COUNT(*) AS total_companies
FROM companies;

-- Top 10 companies by Face Value
SELECT company_name,face_value
FROM companies
ORDER BY face_value DESC
LIMIT 10;

-- Top 10 companies by Book Value
SELECT company_name,book_value
FROM companies
ORDER BY book_value DESC
LIMIT 10;

-- Top 10 companies by Market Capitalization
SELECT company_id,market_cap_crore
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;

-- Top 10 companies by P/E Ratio
SELECT company_id, pe_ratio
FROM market_cap
ORDER BY pe_ratio DESC
LIMIT 10;

-- Top 10 companies by Enterprise value
SELECT company_id, enterprise_value_crore
FROM market_cap
ORDER BY enterprise_value_crore DESC
LIMIT 10;

-- Top 10 companies by Divident Yield
SELECT company_id, dividend_yield_pct
FROM market_cap
ORDER BY dividend_yield_pct DESC
LIMIT 10;

-- Top 10 companies by ROE
SELECT company_name, roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

-- Top 10 companies by ROCE
SELECT company_name, roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;

-- Companies with Lowest P/E Ratio
SELECT company_id, pe_ratio
FROM market_cap
WHERE pe_ratio > 0
ORDER BY pe_ratio ASC
LIMIT 10;

-- Average P/E Ratio
SELECT AVG(pe_ratio) AS average_pe_ratio
FROM market_cap;

-- Average Dividend Yield
SELECT AVG(dividend_yield_pct) AS average_dividend_yield
FROM market_cap;

-- Companies with Face Value greater than 10
SELECT company_name, face_value
FROM companies
WHERE face_value > 10;

-- Companies with Book Value greater than 1000
SELECT company_name, book_value
FROM companies
WHERE book_value > 1000
ORDER BY book_value DESC;

-- Average Market Capitalization
SELECT AVG(market_cap_crore) AS average_market_cap
FROM market_cap;

-- Average Face Value
SELECT AVG(face_value) AS average_face_value
FROM companies;

-- Average Book Value
SELECT AVG(book_value) AS average_book_value
FROM companies;

-- Average ROCE
SELECT AVG(roce_percentage) AS average_roce
FROM companies;

-- Average Enterprise Value
SELECT AVG(enterprise_value_crore) AS average_enterprise_value
FROM market_cap;

-- Average Price to Book Ratio
SELECT AVG(pb_ratio) AS average_pb_ratio
FROM market_cap;

-- Top 10 Companies by Price to Book Ratio
SELECT company_id, pb_ratio
FROM market_cap
ORDER BY pb_ratio DESC
LIMIT 10;

-- Lowest Price to Book Ratio
SELECT company_id, pb_ratio
FROM market_cap
WHERE pb_ratio > 0
ORDER BY pb_ratio ASC
LIMIT 10;

-- Top 10 Companies by EV/EBITDA
SELECT company_id, ev_ebitda
FROM market_cap
ORDER BY ev_ebitda DESC
LIMIT 10;

-- Lowest EV/EBITDA
SELECT company_id, ev_ebitda
FROM market_cap
WHERE ev_ebitda > 0
ORDER BY ev_ebitda ASC
LIMIT 10;

-- Companies with Dividend Yield greater than 3%
SELECT company_id, dividend_yield_pct
FROM market_cap
WHERE dividend_yield_pct > 3
ORDER BY dividend_yield_pct DESC;

-- Companies with Dividend Yield less than 1%
SELECT company_id, dividend_yield_pct
FROM market_cap
WHERE dividend_yield_pct < 1
ORDER BY dividend_yield_pct ASC;