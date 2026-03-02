---
name: shopifyql-setup
description: Interactive setup wizard for ShopifyQL plugin credentials and preferences. Run this once per project to configure your Shopify store connection.
---

You are running the ShopifyQL plugin setup wizard. Your job is to collect credentials and preferences from the user, then write them to `.env` in the project root.

## Step 1 — Check for existing config

Try to read `.env` in the project root.

- If the file exists and has a non-empty `SHOPIFY_STORE_URL`, tell the user their current settings (mask the token: show only the first 8 chars + `...`) and ask: "Would you like to update specific fields, or overwrite everything?"
- If the file does not exist, proceed to collect all fields.

## Step 2 — Collect credentials

Use `AskUserQuestion` to ask ONE question at a time:

**Question 1 — Store URL:**
Ask: "What is your Shopify store URL?"
- Accept formats: `my-store.myshopify.com`, `https://my-store.myshopify.com`, `my-store`
- Normalise to full domain: strip `https://`, strip trailing slashes, append `.myshopify.com` if no dot present

**Question 2 — Access Token:**
Ask: "Paste your Admin API access token (from your Custom App in Shopify Partners)."
- Warn if it doesn't start with `shpat_`
- Never display the full token back to the user after collection

## Step 3 — Write the .env file

Write `.env` in the project root with this exact format:

```
SHOPIFY_STORE_URL=<value>
SHOPIFY_ACCESS_TOKEN=<value>
```

Preserve any other existing lines in `.env` that aren't being updated.

## Step 4 — Confirm

Tell the user:
- Setup complete. Store: `<store_url>`. Token saved (masked).
- "Your credentials are saved to `.env` (gitignored). Do not commit this file."
- "To run a query, just ask: 'run this ShopifyQL query: FROM sales SHOW net_sales SINCE ...'"
- "Or use the executor directly: `python3.11 scripts/execute_query.py --query \"...\"`"

## Error handling

- If Write fails due to permissions, tell the user to create `.env` manually using the template at `scripts/shopifyql.local.md.template`.
- If the token doesn't start with `shpat_`, warn but still save — Custom App tokens may vary.
