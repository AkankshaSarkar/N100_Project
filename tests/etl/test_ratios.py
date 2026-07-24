from src.ratios import (
    net_profit_margin,
    operating_profit_margin,
    roe,
    roce,
    roa,
    debt_to_equity,
    interest_coverage,
    asset_turnover,
    debt_free,
    icr_warning,
    free_cash_flow,
    cfo_quality,
    capex_intensity,
    fcf_conversion_rate,
)

def test_net_profit_margin():
    assert net_profit_margin(20, 100) == 20

def test_net_profit_margin_zero_sales():
    assert net_profit_margin(20, 0) is None

def test_operating_profit_margin():
    assert operating_profit_margin(30, 150) == 20

def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(30, 0) is None

def test_roe():
    assert roe(50, 250) == 20

def test_roe_negative_equity():
    assert roe(50, -10) is None

def test_roce():
    assert roce(40, 200) == 20

def test_roce_zero_capital():
    assert roce(40, 0) is None

def test_roa():
    assert roa(30, 150) == 20

def test_roa_zero_assets():
    assert roa(30, 0) is None

def test_debt_to_equity():
    assert debt_to_equity(100, 50) == 2

def test_debt_to_equity_zero_equity():
    assert debt_to_equity(100, 0) is None

def test_interest_coverage():
    assert interest_coverage(200, 50) == 4

def test_interest_coverage_zero_interest():
    assert interest_coverage(200, 0) is None

def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2

def test_asset_turnover_zero_assets():
    assert asset_turnover(1000, 0) is None

def test_debt_free():
    assert debt_free(0) is True

def test_not_debt_free():
    assert debt_free(10) is False

def test_icr_warning():
    assert icr_warning(1.2) is True

def test_icr_safe():
    assert icr_warning(2.5) is False

from src.ratios import free_cash_flow

def test_free_cash_flow():
    assert free_cash_flow(1000, -300) == 700

def test_free_cash_flow_negative():
    assert free_cash_flow(500, -700) == -200

def test_cfo_quality():
    assert cfo_quality(120, 100) == 1.2

def test_cfo_quality_zero_pat():
    assert cfo_quality(100, 0) is None

def test_capex_intensity():
    assert capex_intensity(20, 100) == 20

def test_capex_intensity_zero_cfo():
    assert capex_intensity(20, 0) is None

def test_fcf_conversion_rate():
    assert fcf_conversion_rate(80, 100) == 80

def test_fcf_conversion_rate_zero_op():
    assert fcf_conversion_rate(80, 0) is None