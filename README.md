# ShopifyQL & Segment Query Language Skill for Claude Code

A Claude Code plugin for writing, executing, debugging, and explaining **ShopifyQL analytics queries** and **Shopify Segment Query Language** customer filters — directly against your live Shopify store, no manual SQL or dashboard switching required.

Use it to automate Shopify ecommerce reporting, build AI-powered analytics workflows, and translate plain-English business questions into structured store queries.

---

## What is ShopifyQL?

ShopifyQL is a SQL-like querying language designed specifically for **Shopify Plus merchants** to analyze store data — including sales, inventory, and customer behavior — without needing advanced coding skills.

It supports powerful features such as time-based filtering, data visualization, and automatic period comparisons. ShopifyQL is accessed via ShopifyQL Notebooks, Shopify Analytics reports, or the GraphQL Admin API.

### ShopifyQL Syntax Basics

ShopifyQL uses structured commands similar to SQL:

| Clause | Purpose | Example |
|---|---|---|
| `FROM` | Data source | `FROM sales` |
| `SHOW` | Metrics to return | `SHOW net_sales, orders_count` |
| `WHERE` | Filter by dimensions | `WHERE sales_channel = 'online_store'` |
| `GROUP BY` | Group results | `GROUP BY product_title` |
| `HAVING` | Filter by metrics (not `WHERE`) | `HAVING net_sales > 1000` |
| `TIMESERIES` | Data over time | `TIMESERIES day` |
| `SINCE` / `UNTIL` | Date range | `SINCE 2026-01-01 UNTIL 2026-01-31` |
| `COMPARE TO` | Period comparison | `COMPARE TO previous_year` |
| `ORDER BY` | Sort results | `ORDER BY net_sales DESC` |
| `LIMIT` | Limit rows | `LIMIT 20` |

### Powerful ShopifyQL Features

- **`DURING`** — time range shorthand (`DURING last_30_days`)
- **`COMPARE TO`** — automatic period comparison (`COMPARE TO previous_period`, `previous_year`)
- **`TIMESERIES`** — aggregate data over time (`TIMESERIES week`)
- **`VISUALIZE`** — declare chart type for Shopify Notebooks
- **`WITH` modifiers** — control rounding, currency display, and more
- **Semi-joins** — filter using subqueries
- **Math on metrics** — `(net_sales / orders_count) AS average_order_value`
- **`TOP N`** — return top N results per group

---

## What this Skill Does

Triggers automatically when you ask Claude to:
- Write a ShopifyQL report query (`FROM sales SHOW ...`)
- **Run or execute a query against your live Shopify store**
- Build a Shopify customer segment filter
- Debug a ShopifyQL syntax error
- Translate a business question into a Shopify analytics query
- Understand available ShopifyQL tables, dimensions, or metrics
- Automate ecommerce reporting with an AI agent

### Coverage

- **ShopifyQL** — full query structure, strict keyword ordering, all clauses (`WHERE`, `GROUP BY`, `TIMESERIES`, `HAVING`, `COMPARE TO`, `VISUALIZE`, `WITH` modifiers, semi-joins, math on metrics, `TOP N`)
- **Segment Query Language** — all attribute types, operators, date formats, and functions (`products_purchased`, `orders_placed`, `shopify_email`, `anniversary`, `customer_within_distance`, `storefront_event`)
- **Common ecommerce patterns** — top products, channel attribution, re-engagement, high-value customers, wholesale/B2B segments
- **Debugging checklist** — ordered list of the most common ShopifyQL errors

---

## Common ShopifyQL Usage Areas

### Analytics Reports
Build tailored reports within Shopify Analytics — top products, revenue by channel, sales trends over time.

```
FROM sales
SHOW net_sales, orders_count
GROUP BY sales_channel
SINCE 2026-01-01 UNTIL 2026-03-31
ORDER BY net_sales DESC
```

### Customer Segmentation
Modify and query customer data segments — repeat vs. new buyers, high-value customers, re-engagement targets.

```
FROM customers
SHOW customer_count
WHERE customer_type = 'returning'
GROUP BY customer_cohort_month
TIMESERIES month
```

### Comparing Sales Periods
Use `COMPARE TO` for automatic period comparisons — no manual date math needed.

```
FROM sales
SHOW net_sales, orders_count
SINCE 2026-01-01 UNTIL 2026-03-31
COMPARE TO previous_year
```

### App Development
Leverage the GraphQL Admin API to fetch ShopifyQL data programmatically — for custom dashboards, reporting apps, and agentic pipelines.

---

## Common ShopifyQL Mistakes (and How to Avoid Them)

### 1. Double quotes instead of single quotes
ShopifyQL requires **single quotes** for string values.

```
-- Wrong
WHERE sales_channel = "online_store"

-- Correct
WHERE sales_channel = 'online_store'
```

### 2. Filtering on metrics in `WHERE` instead of `HAVING`
`WHERE` filters dimensions (text/category fields). `HAVING` filters metrics (numbers).

```
-- Wrong (net_sales is a metric)
WHERE net_sales > 1000

-- Correct
HAVING net_sales > 1000
```

### 3. Missing `GROUP BY` when showing dimensions
If you `SHOW` a dimension alongside a metric, you must `GROUP BY` that dimension.

```
-- Wrong
FROM sales SHOW net_sales, product_title

-- Correct
FROM sales SHOW net_sales, product_title GROUP BY product_title
```

### 4. Rate Limits — 429 errors
ShopifyQL enforces rate limits. If you hit a `429 Too Many Requests` error, you must wait **60 seconds** before retrying. The executor agent handles this automatically with a backoff retry.

---

## Execution

This plugin can execute ShopifyQL queries directly against your Shopify store.

### Requirements

- Python 3.11: `brew install python@3.11`
- Dependencies: `pip3.11 install 'shopifyql[all]' pandas python-dotenv certifi`
- A Shopify Custom App with scopes: `read_analytics`, `read_reports`, `read_customers`, `read_orders`

### Setup

Credentials must be available as **OS environment variables** before launching Claude. The script reads them directly from the environment — it does not load `.env` files.

Export them in your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export SHOPIFY_STORE_URL=my-store.myshopify.com
export SHOPIFY_ACCESS_TOKEN=shpat_xxxx
```

Or pass them inline when launching Claude:

```bash
SHOPIFY_STORE_URL=my-store.myshopify.com SHOPIFY_ACCESS_TOKEN=shpat_xxxx claude
```

For guided setup, run once per project:

```
/shopifyql-setup
```

### Usage

1. Ask Claude to write a ShopifyQL query
2. Say **"run it"** or **"execute"** — the `shopifyql-executor` agent takes over
3. Results ≤ 20 rows appear as a table in chat; larger results are saved as CSV to `./shopifyql-results/`

### Running the script directly

```bash
python3.11 scripts/execute_query.py \
  --query "FROM sales SHOW net_sales SINCE 2026-01-01 UNTIL 2026-01-31"

# For _ms duration columns (LCP, INP):
python3.11 scripts/execute_query.py --raw \
  --query "FROM web_performance SHOW lcp_p75_ms GROUP BY day TIMESERIES day SINCE 2026-01-01 UNTIL 2026-01-31"

# CSV output:
python3.11 scripts/execute_query.py --output csv \
  --query "FROM sales SHOW net_sales GROUP BY product_title SINCE 2026-01-01 UNTIL 2026-01-31 ORDER BY net_sales DESC LIMIT 20"
```

### Known SDK quirk

Columns ending in `_ms` (`lcp_p75_ms`, `inp_p75_ms`) trigger a type-cast bug in `query_pandas()`. Use `--raw` for these — the executor agent handles this automatically.

---

## Installation

### Claude Code Marketplace

Install directly from the Claude Code plugin marketplace:

```bash
/plugin marketplace add devkindhq/shopifyql-skill
/plugin install shopifyql@shopifyql-skill
```

Supports Claude Code CLI, VS Code extension, JetBrains extension, and the Claude.ai web app.

### Manual

Clone this repo and point Claude Code at it, or copy `skills/shopifyql/SKILL.md` into your own plugin.

---

## Further Reading

- [ShopifyQL overview — Shopify Dev Docs](https://shopify.dev/docs/apps/build/shopifyql)
- [ShopifyQL Notebooks — Shopify Help Center](https://help.shopify.com/en/manual/reports-and-analytics/shopify-reports/report-types/shopifyql-editor)
- [I built a Claude Code skill for ShopifyQL — dev.to](https://dev.to/alikazim/i-built-a-claude-code-skill-for-shopifyql-54dc)

---

## Built by Devkind

This plugin was built and is maintained by **[Devkind](https://devkind.com.au)** — a Melbourne-based development and AI agency specialising in Shopify, custom web applications, and agentic AI systems.

### Agentic reporting for Shopify

Devkind builds agentic reporting pipelines that go beyond standard Shopify Analytics dashboards. Instead of switching between tabs and manually interpreting numbers, an AI agent does the analytical heavy lifting — pulling data from Shopify, ad platforms, and Google Analytics, then surfacing what changed, why, and what to do next.

This ShopifyQL plugin is one piece of that stack. If you want:
- Automated daily Shopify analytics reports delivered to Slack or email
- Cross-channel attribution (Shopify + Meta + Google Ads unified)
- A custom AI analytics agent for your ecommerce store
- ShopifyQL dashboards and Segment Query Language automation

...Devkind can scope and build it for you.

## Get in touch

- **Website:** [devkind.com.au](https://devkind.com.au)
- **Email:** [ali@devkind.com.au](mailto:ali@devkind.com.au)

## License

MIT
