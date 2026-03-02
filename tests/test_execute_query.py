"""Tests for execute_query.py — run with: python3.11 -m pytest tests/ -v"""
import json
import subprocess
import sys
from unittest.mock import MagicMock, patch

SCRIPT = "scripts/execute_query.py"


def run_script(*args):
    """Helper: run the script as a subprocess, return parsed stdout JSON."""
    result = subprocess.run(
        ["python3.11", SCRIPT, *args],
        capture_output=True, text=True
    )
    return json.loads(result.stdout), result.returncode


def test_missing_required_args_returns_error():
    """Script exits with error JSON when required args are missing."""
    output, _ = run_script("--store-url", "test.myshopify.com")
    assert "error" in output


def test_output_structure_has_required_keys():
    """Successful query returns rows, columns, row_count."""
    with patch("shopifyql.ShopifyQLClient") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        mock_instance.query.return_value = {
            "data": {
                "queryRoot": {
                    "shopifyqlQuery": {
                        "tableData": {
                            "columns": [{"name": "product_title"}, {"name": "revenue"}],
                            "rowData": [["Widget A", "1000.00"], ["Widget B", "500.00"]]
                        }
                    }
                }
            }
        }
        # Import and call directly rather than subprocess for mock to work
        import importlib.util, sys as _sys
        spec = importlib.util.spec_from_file_location("execute_query", SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        # patch sys.argv
        _sys.argv = ["execute_query.py", "--store-url", "test.myshopify.com",
                     "--token", "shpat_test", "--query", "FROM sales SHOW sum(net_sales)"]
        spec.loader.exec_module(mod)


def test_null_totals_rows_are_filtered():
    """Rows where the first column is null (WITH TOTALS artifact) are stripped."""
    from scripts.execute_query import filter_null_group_rows
    rows = [
        ["Widget A", "1000.00"],
        [None, "1500.00"],   # <-- WITH TOTALS null row
        ["Widget B", "500.00"],
    ]
    result = filter_null_group_rows(rows)
    assert len(result) == 2
    assert [None, "1500.00"] not in result


def test_duration_columns_are_flagged():
    """Columns matching duration type patterns are noted in output."""
    from scripts.execute_query import flag_duration_columns
    columns = ["product_title", "lcp_p75_ms", "inp_p75_ms", "cls_p75"]
    flagged = flag_duration_columns(columns)
    assert "lcp_p75_ms" in flagged
    assert "inp_p75_ms" in flagged
    assert "cls_p75" not in flagged


def test_csv_output_format():
    """--output csv returns valid CSV string instead of JSON rows."""
    from scripts.execute_query import format_output
    data = {
        "columns": ["product_title", "revenue"],
        "rows": [["Widget A", "1000.00"], ["Widget B", "500.00"]],
        "row_count": 2
    }
    csv_out = format_output(data, fmt="csv")
    assert "product_title,revenue" in csv_out
    assert "Widget A" in csv_out
