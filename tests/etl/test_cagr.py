import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.cagr import (
    cagr,
    revenue_cagr,
    profit_cagr,
    eps_cagr,
)


def test_cagr():
    result = cagr(100, 121, 2)
    assert round(result, 2) == 10.00


def test_cagr_zero_years():
    assert cagr(100, 121, 0) is None


def test_cagr_negative_start():
    assert cagr(-100, 121, 2) is None


def test_cagr_negative_end():
    assert cagr(100, -121, 2) is None


def test_revenue_cagr():
    result = revenue_cagr(100, 121, 2)
    assert round(result, 2) == 10.00


def test_profit_cagr():
    result = profit_cagr(100, 144, 2)
    assert round(result, 2) == 20.00


def test_eps_cagr():
    result = eps_cagr(10, 12.1, 2)
    assert round(result, 2) == 10.00


def test_revenue_cagr_zero_year():
    assert revenue_cagr(100, 120, 0) is None


def test_profit_cagr_invalid():
    assert profit_cagr(-50, 100, 5) is None


def test_eps_cagr_invalid():
    assert eps_cagr(0, 20, 5) is None