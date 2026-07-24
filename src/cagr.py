def cagr(start_value, end_value, years):
    if years <= 0:
        return None
    if start_value <= 0 or end_value <= 0:
        return None
    return ((end_value / start_value) ** (1 / years) - 1) * 100


def revenue_cagr(start_revenue, end_revenue, years):
    return cagr(start_revenue, end_revenue, years)


def profit_cagr(start_profit, end_profit, years):
    return cagr(start_profit, end_profit, years)


def eps_cagr(start_eps, end_eps, years):
    return cagr(start_eps, end_eps, years)