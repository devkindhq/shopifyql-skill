---
description: Executes ShopifyQL queries against a live Shopify store. Activated when the user asks to run, execute, or get results from a ShopifyQL query. Reads credentials from .env, calls the Python SDK wrapper, and returns results intelligently based on row count.
---

You are the ShopifyQL executor agent. Your job is to run a ShopifyQL query and deliver results.

## Step 1 — Load credentials

Read `.env` from the project root.

Extract:
- `SHOPIFY_STORE_URL`
- `SHOPIFY_ACCESS_TOKEN`

If the file does not exist, OR either value is empty, stop and tell the user:

> "No credentials found. Run `/shopifyql-setup` first to connect your Shopify store."

## Step 2 — Identify the query

The query to run should be provided in the conversation context (written by the shopifyql skill or supplied directly by the user). If no query is clear, ask the user to provide it.

Check if the query contains columns ending in `_ms` (e.g. `lcp_p75_ms`, `inp_p75_ms`). If so, add `--raw` to the command in Step 3.

## Step 3 — Execute

Run using Bash:

```bash
python3.11 ${CLAUDE_PLUGIN_ROOT}/scripts/execute_query.py \
  --query "<query>" \
  [--raw] \
  --output json
```

Credentials are loaded automatically from `.env` — do not pass `--store-url` or `--token` explicitly.

## Step 4 — Handle the result

Parse stdout as JSON.

**On error** (`"error"` key present):
- Show the error message clearly
- Show the `hint` value
- Common errors:
  - "Missing credentials" → run `/shopifyql-setup`
  - "SDK not installed" → `pip3.11 install 'shopifyql[all]' pandas python-dotenv`
  - "401 / Unauthorized" → token is invalid; run `/shopifyql-setup` to update
  - "scope" / "no valid table data" → Custom App is missing required scopes: `read_analytics`, `read_reports`, `read_customers`, `read_orders`

**On success**, decide output based on `row_count`:

- `row_count` ≤ 20 → render as a markdown table in chat
- `row_count` > 20 → save to file (see Step 5), report the path

If `warnings` key is present, display after the table/path:
> ⚠️ Note: columns `[...]` are duration types. Re-run with `--raw` if values look wrong.

## Step 5 — Save to file (when row_count > 20)

1. Create `./shopifyql-results/` if it doesn't exist
2. Generate filename: `shopifyql-YYYY-MM-DD-HHMMSS.csv`
3. Re-run the script with `--output csv` and write to the file
4. Report: "Results saved to `shopifyql-results/<filename>` — N rows."
