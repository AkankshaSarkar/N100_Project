from pathlib import Path
import pandas as pd

def test_validator_file_exists():
    assert Path("src/validator.py").exists()


def test_database_exists():
    assert Path("db/nifty100.db").exists()


def test_output_folder_exists():
    assert Path("output").exists()


def test_load_audit_exists():
    assert Path("output/load_audit.csv").exists()


def test_validation_failures_exists():
    assert Path("output/validation_failures.csv").exists()


def test_notebooks_exists():
    assert Path("notebooks").exists()


def test_exploratory_sql_exists():
    assert Path("notebooks/exploratory_queries.sql").exists()


def test_schema_exists():
    assert Path("sql/schema.sql").exists()

def test_load_audit_not_empty():
    df = pd.read_csv("output/load_audit.csv")
    assert len(df) > 0


def test_validation_not_empty():
    df = pd.read_csv("output/validation_failures.csv")
    assert len(df) > 0


def test_load_audit_has_table_name():
    df = pd.read_csv("output/load_audit.csv")
    assert "table_name" in df.columns


def test_load_audit_has_row_count():
    df = pd.read_csv("output/load_audit.csv")
    assert "row_count" in df.columns


def test_load_audit_has_status():
    df = pd.read_csv("output/load_audit.csv")
    assert "status" in df.columns


def test_validation_has_rule():
    df = pd.read_csv("output/validation_failures.csv")
    assert "rule" in df.columns


def test_validation_has_status():
    df = pd.read_csv("output/validation_failures.csv")
    assert "status" in df.columns