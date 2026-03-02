"""Tests for execute_query.py — run with: python3.11 -m pytest tests/ -v"""
import json
import subprocess
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

SCRIPT = "scripts/execute_query.py"


def run_script(*args):
    """Helper: run the script as a subprocess, return parsed stdout JSON."""
    result = subprocess.run(
        ["python3.11", SCRIPT, *args],
        capture_output=True, text=True
    )
    return json.loads(result.stdout), result.returncode


def test_missing_required_args_returns_error():
    """Script exits with error JSON when --query is missing."""
    output, _ = run_script("--store-url", "test.myshopify.com", "--token", "shpat_x")
    assert "error" in output


def test_missing_credentials_returns_error():
    """Script exits with error JSON when credentials are explicitly empty."""
    output, code = run_script("--store-url", "", "--token", "",
                              "--query", "FROM sales SHOW net_sales")
    assert "error" in output
    assert code == 1


def test_output_structure_has_required_keys():
    """Successful query returns columns, rows, row_count."""
    mock_df = pd.DataFrame({
        "product_title": ["Widget A", "Widget B"],
        "net_sales": ["1000.00", "500.00"],
    })
    with patch("shopifyql.ShopifyQLClient") as mock_client_cls:
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client
        mock_client.query_pandas.return_value = mock_df

        from scripts.execute_query import execute_query
        result = execute_query("test.myshopify.com", "shpat_test",
                               "FROM sales SHOW net_sales")

    assert "columns" in result
    assert "rows" in result
    assert "row_count" in result
    assert result["row_count"] == 2
    assert result["columns"] == ["product_title", "net_sales"]


def test_null_totals_rows_are_filtered():
    """Rows where the first column is null (WITH TOTALS artifact) are stripped."""
    from scripts.execute_query import filter_null_group_rows
    rows = [
        ["Widget A", "1000.00"],
        [None, "1500.00"],   # WITH TOTALS null row
        ["Widget B", "500.00"],
    ]
    result = filter_null_group_rows(rows)
    assert len(result) == 2
    assert [None, "1500.00"] not in result


def test_duration_columns_are_flagged():
    """Columns ending in _ms are flagged; others are not."""
    from scripts.execute_query import flag_duration_columns
    columns = ["product_title", "lcp_p75_ms", "inp_p75_ms", "cls_p75"]
    flagged = flag_duration_columns(columns)
    assert "lcp_p75_ms" in flagged
    assert "inp_p75_ms" in flagged
    assert "cls_p75" not in flagged


def test_csv_output_format():
    """format_output with fmt='csv' returns valid CSV with headers."""
    from scripts.execute_query import format_output
    data = {
        "columns": ["product_title", "revenue"],
        "rows": [["Widget A", "1000.00"], ["Widget B", "500.00"]],
        "row_count": 2
    }
    csv_out = format_output(data, fmt="csv")
    assert "product_title,revenue" in csv_out
    assert "Widget A" in csv_out


def test_normalize_shop_strips_domain():
    """_normalize_shop accepts full URL or bare subdomain."""
    from scripts.execute_query import _normalize_shop
    assert _normalize_shop("my-store.myshopify.com") == "my-store"
    assert _normalize_shop("https://my-store.myshopify.com/") == "my-store"
    assert _normalize_shop("my-store") == "my-store"


def test_clean_query_strips_visualize():
    """_clean_query removes VISUALIZE lines that the API rejects."""
    from scripts.execute_query import _clean_query
    q = "FROM sales\nSHOW net_sales\nVISUALIZE bar\nSINCE 2026-01-01"
    cleaned = _clean_query(q)
    assert "VISUALIZE" not in cleaned
    assert "FROM sales" in cleaned
