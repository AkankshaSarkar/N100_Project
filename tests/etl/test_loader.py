from pathlib import Path

def test_loader_exists():
    assert Path("src/loader.py").exists()

def test_data_folder_exists():
    assert Path("Data").exists()

def test_raw_folder_exists():
    assert Path("Data/raw").exists()

def test_database_exists():
    assert Path("db/nifty100.db").exists()

def test_output_folder_exists():
    assert Path("output").exists()

def test_load_audit_exists():
    assert Path("output/load_audit.csv").exists()

def test_validation_file_exists():
    assert Path("output/validation_failures.csv").exists()

def test_notebooks_exists():
    assert Path("notebooks").exists()

def test_sql_folder_exists():
    assert Path("sql").exists()

def test_schema_exists():
    assert Path("sql/schema.sql").exists()

def test_exploratory_sql_exists():
    assert Path("notebooks/exploratory_queries.sql").exists()

def test_tests_folder_exists():
    assert Path("tests/etl").exists()