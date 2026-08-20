from pathlib import Path
import pandas as pd


OUTPUT_DIR = Path("output")


def test_validation_failures_file_exists():
    """Validation output file should exist."""
    assert (OUTPUT_DIR / "validation_failures.csv").exists()


def test_validation_failures_has_required_columns():
    """Validation report should contain rule, severity and status."""
    file = OUTPUT_DIR / "validation_failures.csv"

    if not file.exists():
        return

    df = pd.read_csv(file)

    required_columns = {"rule", "severity", "status"}

    assert required_columns.issubset(df.columns)


def test_validation_status_is_valid():
    """Validation status should be PASS or FAIL."""
    file = OUTPUT_DIR / "validation_failures.csv"

    if not file.exists():
        return

    df = pd.read_csv(file)

    assert df["status"].isin(["PASS", "FAIL"]).all()


def test_no_duplicate_rows_in_cluster_labels():
    """Cluster labels output should not contain duplicate rows."""
    file = OUTPUT_DIR / "cluster_labels.csv"

    if not file.exists():
        return

    df = pd.read_csv(file)

    assert not df.duplicated().any()


def test_company_name_not_null():
    """Company names should not be NULL."""
    file = OUTPUT_DIR / "cluster_profile.csv"

    if not file.exists():
        return

    df = pd.read_csv(file)

    if "company_name" in df.columns:
        assert df["company_name"].notna().all()


def test_broad_sector_not_null():
    """Broad sector should not be NULL."""
    file = OUTPUT_DIR / "cluster_profile.csv"

    if not file.exists():
        return

    df = pd.read_csv(file)

    if "broad_sector" in df.columns:
        assert df["broad_sector"].notna().all()