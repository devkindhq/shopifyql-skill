#!/usr/bin/env python3.11
"""
ShopifyQL query executor — wraps the official Shopify Python SDK.

Usage:
    python3.11 scripts/execute_query.py \\
        --query "FROM sales SHOW net_sales SINCE 2026-01-01 UNTIL 2026-01-31" \\
        [--raw]            # use raw client.query() for _ms duration columns
        [--output json|csv]

Credentials loaded from .env (project root):
    SHOPIFY_STORE_URL=my-store.myshopify.com
    SHOPIFY_ACCESS_TOKEN=shpat_xxxx

Output (stdout): JSON object with keys: columns, rows, row_count, [warnings]
On error (stdout): JSON object with keys: error, hint
"""
import argparse
import csv
import io
import json
import os
import sys
import time
from pathlib import Path

import certifi

os.environ.setdefault("SSL_CERT_FILE", certifi.where())
os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

DURATION_COLUMN_PATTERNS = ("_ms",)
RATE_LIMIT_BACKOFF = 30  # seconds to wait after a rate-limit error


def flag_duration_columns(columns: list[str]) -> list[str]:
    """Return column names that match known duration-type patterns."""
    return [c for c in columns if any(c.endswith(p) for p in DURATION_COLUMN_PATTERNS)]


def filter_null_group_rows(rows: list[list]) -> list[list]:
    """Remove rows where the first column is null — artifact of WITH TOTALS."""
    return [row for row in rows if row and row[0] is not None]


def _json_safe(val):
    """Convert pandas/numpy types that json.dumps can't handle."""
    import pandas as pd
    import numpy as np
    if isinstance(val, (pd.Timestamp,)):
        return val.isoformat()
    if isinstance(val, (np.integer,)):
        return int(val)
    if isinstance(val, (np.floating,)):
        return float(val)
    if isinstance(val, float) and (val != val):  # NaN
        return None
    return val


def format_output(data: dict, fmt: str = "json") -> str:
    """Format result data as JSON or CSV string."""
    if fmt == "csv":
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(data["columns"])
        writer.writerows(data["rows"])
        return buf.getvalue()
    safe = {**data, "rows": [[_json_safe(v) for v in row] for row in data["rows"]]}
    return json.dumps(safe, indent=2)


def _normalize_shop(store_url: str) -> str:
    """Strip https://, trailing slashes, and .myshopify.com — SDK wants bare subdomain."""
    shop = store_url.strip().rstrip("/")
    shop = shop.replace("https://", "").replace("http://", "")
    if shop.endswith(".myshopify.com"):
        shop = shop[: -len(".myshopify.com")]
    return shop


def _clean_query(query: str) -> str:
    """Strip VISUALIZE lines — UI-only hints rejected by the API."""
    return "\n".join(
        line for line in query.splitlines()
        if not line.strip().startswith("VISUALIZE")
    ).strip()


def execute_query(store_url: str, token: str, query: str, raw: bool = False) -> dict:
    """Run query via ShopifyQL SDK. raw=True uses client.query() for _ms columns."""
    try:
        import pandas as pd
        from shopifyql import ShopifyQLClient
    except ImportError as e:
        return {
            "error": f"Missing dependency: {e}",
            "hint": "Run: pip3.11 install 'shopifyql[all]' pandas python-dotenv"
        }

    shop = _normalize_shop(store_url)
    client = ShopifyQLClient(shop=shop, access_token=token)
    q = _clean_query(query)

    _GQL = """
    query ($q: String!) {
        shopifyqlQuery(query: $q) {
            tableData { columns { name dataType } rows }
            parseErrors
        }
    }
    """

    def _run():
        if raw:
            # Bypass ShopifyQLRecordsResult type-casting (breaks on _ms columns)
            # by calling graphql_query directly and reading the JSON scalar rows
            resp = client.graphql_query(_GQL, variables={"q": q})
            td = resp["data"]["shopifyqlQuery"]["tableData"]
            cols = [c["name"] for c in td["columns"]]
            rows_raw = td["rows"]  # list of dicts
            return pd.DataFrame([[r[c] for c in cols] for r in rows_raw], columns=cols)
        return client.query_pandas(q)

    try:
        df = _run()
    except Exception as e:
        err_str = str(e)
        if "Rate limited" in err_str:
            time.sleep(RATE_LIMIT_BACKOFF)
            try:
                df = _run()
            except Exception as e2:
                return {"error": str(e2), "hint": _error_hint(str(e2))}
        else:
            return {"error": err_str, "hint": _error_hint(err_str)}

    raw_columns = list(df.columns)
    raw_rows = df.values.tolist()
    rows = filter_null_group_rows(raw_rows)
    flagged = flag_duration_columns(raw_columns)

    result = {
        "columns": raw_columns,
        "rows": rows,
        "row_count": len(rows),
    }
    if flagged:
        result["warnings"] = [
            f"Column(s) {flagged} are duration types. "
            "If values look wrong, re-run with --raw."
        ]
    return result


def _error_hint(err: str) -> str:
    if "401" in err or "Unauthorized" in err:
        return "Token invalid or expired. Check SHOPIFY_ACCESS_TOKEN in .env"
    if "404" in err:
        return "Store URL not found. Check SHOPIFY_STORE_URL in .env"
    if "scope" in err.lower() or "permission" in err.lower() or "no valid table data" in err.lower():
        return "Missing API scope. Enable read_analytics, read_reports, read_customers, read_orders on your Custom App."
    return "Check SHOPIFY_STORE_URL and SHOPIFY_ACCESS_TOKEN in .env are correct."


def main():
    parser = argparse.ArgumentParser(description="Execute a ShopifyQL query.")
    parser.add_argument("--store-url", default=os.environ.get("SHOPIFY_STORE_URL"),
                        help="e.g. my-store.myshopify.com (or set SHOPIFY_STORE_URL in .env)")
    parser.add_argument("--token", default=os.environ.get("SHOPIFY_ACCESS_TOKEN"),
                        help="Admin API access token (or set SHOPIFY_ACCESS_TOKEN in .env)")
    parser.add_argument("--query", required=True, help="ShopifyQL query string")
    parser.add_argument("--output", choices=["json", "csv"], default="json")
    parser.add_argument("--raw", action="store_true",
                        help="Use raw client.query() — required for _ms duration columns")
    try:
        args = parser.parse_args()
    except SystemExit:
        print(json.dumps({"error": "Missing required arguments: --query"}))
        sys.exit(1)

    if not args.store_url or not args.token:
        print(json.dumps({
            "error": "Missing credentials",
            "hint": "Set SHOPIFY_STORE_URL and SHOPIFY_ACCESS_TOKEN in .env"
        }))
        sys.exit(1)

    result = execute_query(args.store_url, args.token, args.query, raw=args.raw)

    if "error" in result:
        print(json.dumps(result))
        sys.exit(1)

    print(format_output(result, fmt=args.output))


if __name__ == "__main__":
    main()
