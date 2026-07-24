def net_profit_margin(net_profit, sales):
    if sales == 0:
        return None
    return (net_profit / sales) * 100


def operating_profit_margin(op_profit, sales):
    if sales == 0:
        return None
    return (op_profit / sales) * 100


def roe(net_profit, equity):
    if equity <= 0:
        return None
    return (net_profit / equity) * 100


def roce(ebit, capital_employed):
    if capital_employed <= 0:
        return None
    return (ebit / capital_employed) * 100


def roa(net_profit, total_assets):
    if total_assets == 0:
        return None
    return (net_profit / total_assets) * 100

def debt_to_equity(borrowings, equity):
    if equity <= 0:
        return None
    return borrowings / equity


def interest_coverage(operating_profit, interest):
    if interest == 0:
        return None
    return operating_profit / interest


def asset_turnover(sales, total_assets):
    if total_assets == 0:
        return None
    return sales / total_assets


def debt_free(borrowings):
    return borrowings == 0


def icr_warning(icr):
    if icr is None:
        return False
    return icr < 1.5

def free_cash_flow(cfo, investing_activity):
    return cfo + investing_activity

def cfo_quality(cfo, pat):
    if pat == 0:
        return None
    return cfo / pat

def capex_intensity(capex, cfo):
    if cfo == 0:
        return None
    return (capex / cfo) * 100

def fcf_conversion_rate(fcf, operating_profit):
    if operating_profit == 0:
        return None
    return (fcf / operating_profit) * 100