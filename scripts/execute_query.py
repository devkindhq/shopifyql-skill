#!/usr/bin/env python3.11
"""
ShopifyQL query executor — wraps the official Shopify Python SDK.

Usage:
    python3.11 scripts/execute_query.py \\
        --store-url my-store.myshopify.com \\
        --token shpat_xxxx \\
        --query "FROM sales SHOW sum(net_sales) DURING last_month" \\
        [--output json|csv]

Output (stdout): JSON object with keys: rows, columns, row_count, [warnings]
On error (stdout): JSON object with keys: error, hint
"""
import argparse
import csv
import io
import json
import sys
import time

DURATION_COLUMN_PATTERNS = ("_ms",)


def flag_duration_columns(columns: list[str]) -> list[str]:
    """Return column names that match known duration-type patterns (SDK bug)."""
    return [c for c in columns if any(c.endswith(p) for p in DURATION_COLUMN_PATTERNS)]


def filter_null_group_rows(rows: list[list]) -> list[list]:
    """Remove rows where the first column is null — artifact of WITH TOTALS."""
    return [row for row in rows if row and row[0] is not None]


def format_output(data: dict, fmt: str = "json") -> str:
    """Format result data as JSON or CSV string."""
    if fmt == "csv":
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(data["columns"])
        writer.writerows(data["rows"])
        return buf.getvalue()
    return json.dumps(data, indent=2)


def execute_query(store_url: str, token: str, query: str) -> dict:
    """Run query via ShopifyQL SDK, handle raw mode and post-processing."""
    try:
        from shopifyql import ShopifyQLClient
    except ImportError:
        return {
            "error": "shopifyql SDK not installed",
            "hint": "Run: pip3.11 install shopifyql"
        }

    client = ShopifyQLClient(shop_url=store_url, access_token=token)

    for attempt in range(2):
        try:
            # Use raw=True to avoid the duration-type cast bug in query_pandas()
            response = client.query(query, raw=True)
            break
        except Exception as e:
            err_str = str(e)
            if "429" in err_str and attempt == 0:
                # Rate limit — wait 60s and retry once
                print(
                    json.dumps({"info": "Rate limit hit (429). Waiting 60s before retry..."}),
                    file=sys.stderr
                )
                time.sleep(60)
                continue
            return {
                "error": err_str,
                "hint": _error_hint(err_str)
            }

    try:
        table = (
            response["data"]["queryRoot"]["shopifyqlQuery"]["tableData"]
        )
        raw_columns = [c["name"] for c in table["columns"]]
        raw_rows = table["rowData"]
    except (KeyError, TypeError) as e:
        return {"error": f"Unexpected response shape: {e}", "hint": "Check SDK version."}

    rows = filter_null_group_rows(raw_rows)
    flagged = flag_duration_columns(raw_columns)

    result = {
        "columns": raw_columns,
        "rows": rows,
        "row_count": len(rows),
    }
    if flagged:
        result["warnings"] = [
            f"Column(s) {flagged} use a duration type the SDK cannot cast. "
            "Values are returned as raw strings."
        ]
    return result


def _error_hint(err: str) -> str:
    if "401" in err or "Unauthorized" in err:
        return "Token invalid or expired. Check your Custom App admin token in Shopify Partners."
    if "404" in err:
        return "Store URL not found. Verify the myshopify.com domain."
    if "python3.11" in err.lower():
        return "Python 3.11 required. Install with: brew install python@3.11"
    return "Check store URL and access token are correct."


def main():
    parser = argparse.ArgumentParser(description="Execute a ShopifyQL query.")
    parser.add_argument("--store-url", required=True, help="e.g. my-store.myshopify.com")
    parser.add_argument("--token", required=True, help="Admin API access token (shpat_...)")
    parser.add_argument("--query", required=True, help="ShopifyQL query string")
    parser.add_argument("--output", choices=["json", "csv"], default="json")
    try:
        args = parser.parse_args()
    except SystemExit:
        print(json.dumps({"error": "Missing required arguments: --store-url, --token, --query"}))
        sys.exit(1)

    result = execute_query(args.store_url, args.token, args.query)

    if "error" in result:
        print(json.dumps(result))
        sys.exit(1)

    print(format_output(result, fmt=args.output))


if __name__ == "__main__":
    main()
