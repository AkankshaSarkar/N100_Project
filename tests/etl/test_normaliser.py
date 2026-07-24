import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

import pandas as pd
from src.normaliser import normalize_ticker, normalize_year


def test_normalize_ticker_uppercase():
    df = pd.DataFrame({"id": ["tcs"]})
    result = normalize_ticker(df)
    assert result["id"][0] == "TCS"


def test_normalize_ticker_spaces():
    df = pd.DataFrame({"id": ["  infy  "]})
    result = normalize_ticker(df)
    assert result["id"][0] == "INFY"


def test_normalize_ticker_already_upper():
    df = pd.DataFrame({"id": ["RELIANCE"]})
    result = normalize_ticker(df)
    assert result["id"][0] == "RELIANCE"


def test_normalize_ticker_numeric():
    df = pd.DataFrame({"id": [123]})
    result = normalize_ticker(df)
    assert result["id"][0] == "123"


def test_normalize_ticker_empty():
    df = pd.DataFrame({"id": [""]})
    result = normalize_ticker(df)
    assert result["id"][0] == ""


def test_normalize_ticker_no_column():
    df = pd.DataFrame({"name": ["ABC"]})
    result = normalize_ticker(df)
    assert "name" in result.columns


def test_normalize_year_integer():
    df = pd.DataFrame({"year": ["2024"]})
    result = normalize_year(df)
    assert result["year"][0] == 2024


def test_normalize_year_float():
    df = pd.DataFrame({"year": ["2024.0"]})
    result = normalize_year(df)
    assert result["year"][0] == 2024


def test_normalize_year_invalid():
    df = pd.DataFrame({"year": ["abcd"]})
    result = normalize_year(df)
    assert pd.isna(result["year"][0])


def test_normalize_year_empty():
    df = pd.DataFrame({"year": [""]})
    result = normalize_year(df)
    assert pd.isna(result["year"][0])


def test_normalize_year_none():
    df = pd.DataFrame({"year": [None]})
    result = normalize_year(df)
    assert pd.isna(result["year"][0])


def test_normalize_year_no_column():
    df = pd.DataFrame({"value": [100]})
    result = normalize_year(df)
    assert "value" in result.columns