---
name: shopifyql
description: >
  Write, debug, and explain ShopifyQL queries and Shopify Segment Query Language expressions.
  Use this skill whenever the user wants to query Shopify analytics data, build customer segments,
  write ShopifyQL for reports, explore sales/orders/products data via the Shopify Admin API,
  debug a ShopifyQL error, understand available tables/dimensions/metrics, or translate a business
  question into a Shopify query. Also triggers for: "ShopifyQL", "Shopify analytics query",
  "customer segment filter", "Shopify segment", "SHOW FROM sales", "GROUP BY in Shopify",
  "Shopify report query", or any mention of ShopifyQL tables like `sales`, `sessions`, `orders`.
---

# ShopifyQL & Segment Query Language

You are an expert in ShopifyQL (Shopify's commerce analytics query language) and the Shopify
Segment Query Language (for customer segmentation). Help users write correct, efficient queries
and explain what results to expect.

---

## 1. ShopifyQL — Analytics Queries

### Required structure

Every ShopifyQL query must have `FROM` and `SHOW`. All other clauses are optional but **must appear
in this exact order**:

```
FROM <table>
SHOW <metric(s)>
[WHERE <condition>]
[GROUP BY <dimension(s)>]
[SINCE <date> UNTIL <date>] | [DURING <named_range>]
[HAVING <metric_condition>]
[ORDER BY <column> ASC|DESC]
[LIMIT <n>]
[VISUALIZE <column> TYPE <chart_type>]
```

Getting the order wrong is the #1 source of ShopifyQL syntax errors. Always verify the order
when debugging.

### Common tables

| Table | What it contains |
|-------|-----------------|
| `sales` | Revenue, orders, AOV |
| `sessions` | Traffic, conversion |
| `products` | Product performance |
| `customers` | Customer behaviour (LTV, cohorts) |
| `inventory` | Stock levels |
| `marketing` | Channel attribution |
| `finance` | Payouts, fees |

Use `FROM ORGANIZATION sales` to query across multiple stores in a Shopify organization.

### WHERE — filtering dimensions

Filters run *before* aggregation (like SQL `WHERE`). Only dimensions, not metrics.

```shopifyql
FROM sales
SHOW sum(net_sales) AS revenue
WHERE billing_country = 'US'
AND product_type != 'Gift Card'
```

String operators: `=`, `!=`, `STARTS WITH`, `ENDS WITH`, `CONTAINS`
Logical: `AND`, `OR`, `NOT`
**Always use single quotes for string values.**

### GROUP BY — segmenting data

Required whenever you include a dimension in `SHOW`.

```shopifyql
FROM sales
SHOW product_title, sum(net_sales) AS revenue
GROUP BY product_title
ORDER BY revenue DESC
LIMIT 10
```

### Date filtering

Two approaches — use whichever fits:

**Relative offsets (SINCE/UNTIL):**
```shopifyql
SINCE -30d UNTIL today
SINCE -1y UNTIL -1d
```

**Named ranges (DURING):**
```shopifyql
DURING last_month
DURING last_year
DURING this_week
```

**TIMESERIES** — groups results by a time dimension:
```shopifyql
FROM sales
SHOW sum(net_sales) AS revenue
TIMESERIES day
SINCE -30d UNTIL today
```
Valid intervals: `hour`, `day`, `week`, `month`, `quarter`, `year`

### HAVING — filtering after aggregation

Like SQL `HAVING`. Filters on metric values after `GROUP BY`.

```shopifyql
FROM sales
SHOW product_title, sum(net_sales) AS revenue, count(orders) AS order_count
GROUP BY product_title
HAVING revenue > 1000
ORDER BY revenue DESC
```

### COMPARE TO — period comparison

```shopifyql
FROM sales
SHOW sum(net_sales) AS revenue
SINCE -30d UNTIL today
COMPARE TO previous_period
```

Options: `previous_period`, `previous_year`, `previous_year_match_day_of_week`

### WITH modifiers

Append `WITH` to add computed columns:

```shopifyql
FROM sales
SHOW sum(net_sales) AS revenue
TIMESERIES month
WITH PERCENT_CHANGE, CUMULATIVE_VALUES
```

Available: `TOTALS`, `GROUP_TOTALS`, `PERCENT_CHANGE`, `CUMULATIVE_VALUES`, `CURRENCY`, `TIMEZONE`

### VISUALIZE

```shopifyql
FROM sales
SHOW product_title, sum(net_sales) AS revenue
GROUP BY product_title
ORDER BY revenue DESC
LIMIT 10
VISUALIZE revenue TYPE bar
```

Chart types: `bar`, `line`, `donut`, `histogram`, `heatmap`, `table`, `single_stat`

### Semi-joins (MATCHES)

Filter by related entities without writing a subquery:

```shopifyql
FROM customers
SHOW customer_id, sum(net_sales)
WHERE products_purchased MATCHES (product_tag = 'sale')
GROUP BY customer_id
```

Functions: `products_purchased`, `orders_placed`, `shopify_email.EVENT()`

### Math on metrics

```shopifyql
FROM sales
SHOW sum(net_sales) / count(orders) AS aov
```

### Aliases

```shopifyql
SHOW sum(net_sales) AS total_revenue, count(orders) AS order_count
```

### TOP N

```shopifyql
FROM sales
SHOW top_5(product_title) AS top_products, sum(net_sales) AS revenue
GROUP BY top_products
```

The remainder is grouped as "Other".

---

## 2. Segment Query Language — Customer Segments

Segment queries are **WHERE-only** — no `FROM`, `SHOW`, or other clauses. They're used exclusively
in the Shopify Customers API and Admin segment builder.

### Basic syntax

```
<attribute> <operator> <value>
```

Multiple conditions:
```
<condition1> AND <condition2> OR <condition3>
```

**AND takes precedence over OR.** Use parentheses to override:
```
email_subscription_status = 'SUBSCRIBED' AND (customer_countries CONTAINS 'US' OR amount_spent > 500)
```

Limits: max 10 clauses per query.

### Operators by data type

| Type | Operators |
|------|-----------|
| Boolean | `=`, `!=` |
| Date | `=`, `!=`, `>`, `>=`, `<`, `<=`, `BETWEEN` |
| Enum | `=`, `!=` |
| Float/Integer | `=`, `!=`, `>`, `>=`, `<`, `<=`, `BETWEEN` |
| String | `=`, `!=` |
| List | `CONTAINS`, `NOT CONTAINS` |
| Function | `MATCHES`, `NOT MATCHES` |

### Date formats

- Absolute: `'2024-01-01'` or `'2024-01-01T16:00:00'`
- Relative offset: `-7d`, `-2w`, `-1m`, `-1y`
- Named: `today`, `yesterday`

```shopifyql
last_order_date > -30d
first_order_date BETWEEN '2024-01-01' AND '2024-12-31'
```

### Core attributes

| Attribute | Type | Example |
|-----------|------|---------|
| `email_subscription_status` | Enum | `= 'SUBSCRIBED'` |
| `sms_subscription_status` | Enum | `= 'SUBSCRIBED'` |
| `amount_spent` | Float | `>= 500.00` |
| `number_of_orders` | Integer | `> 5` |
| `customer_tags` | List | `CONTAINS 'wholesale'` |
| `customer_countries` | List | `CONTAINS 'US'` |
| `customer_cities` | List | `CONTAINS 'New York'` |
| `customer_regions` | List | `CONTAINS 'NY'` |
| `customer_email_domain` | String | `= 'gmail.com'` |
| `customer_language` | String | `= 'en'` |
| `customer_account_status` | Enum | `= 'ENABLED'` |
| `customer_added_date` | Date | `> -90d` |
| `first_order_date` | Date | `< -365d` |
| `last_order_date` | Date | `> -30d` |
| `abandoned_checkout_date` | Date | `> -7d` |
| `predicted_spend_tier` | Enum | `= 'HIGH'` |
| `rfm_group` | Enum | `= 'CHAMPIONS'` |
| `product_subscription_status` | Enum | `= 'SUBSCRIBER'` |

### Function conditions

**products_purchased** — by product ID, tag, or date:
```
products_purchased MATCHES (id IN (1234567890, 9876543210))
products_purchased MATCHES (tag = 'sale', date > -90d)
```

**orders_placed** — by order attributes:
```
orders_placed MATCHES (financial_status = 'paid', date > -30d)
```

**shopify_email.EVENT()** — by email campaign interaction:
```
shopify_email.opened MATCHES (activity_id = 5240029206, date > -30d)
shopify_email.clicked MATCHES (activity_id = 5240029206)
```
Events: `bounced`, `clicked`, `delivered`, `marked_as_spam`, `opened`, `unsubscribed`

**anniversary()** — yearly recurring dates (e.g. birthdays):
```
anniversary() MATCHES (date = today, attribute = 'birthdate')
```

**customer_within_distance()** — geo-proximity:
```
customer_within_distance() MATCHES (lat = -33.8688, lng = 151.2093, distance = 50, unit = 'km')
```

**storefront_event** — browsing behaviour:
```
storefront_event.product_viewed MATCHES (product_id = 1234567890, date > -7d)
storefront_event.collection_viewed MATCHES (collection_id = 987654321)
```

**store_credit_accounts** — customers with store credit:
```
store_credit_accounts MATCHES (balance > 0)
```

---

## 3. Query writing workflow

When a user asks a business question, follow this process:

1. **Identify the goal** — analytics report (ShopifyQL) or customer segment (Segment QL)?
2. **Pick the table** — for ShopifyQL, identify the correct `FROM` table
3. **Identify metrics vs dimensions** — metrics go in `SHOW` with aggregations; dimensions go in
   `GROUP BY` (and also in `SHOW`)
4. **Add filters** — `WHERE` for pre-aggregation, `HAVING` for post-aggregation
5. **Set the date range** — always include one unless the user wants all-time data
6. **Verify keyword order** — `FROM → SHOW → WHERE → GROUP BY → SINCE/UNTIL → HAVING → ORDER BY → LIMIT`
7. **Add visualisation** if the user wants a chart

---

## 4. Common ecommerce patterns

Reusable starting points for typical Shopify store analytics and segmentation:

**Top revenue products this month:**
```shopifyql
FROM sales
SHOW product_title, sum(net_sales) AS revenue, count(orders) AS orders
GROUP BY product_title
DURING last_month
ORDER BY revenue DESC
LIMIT 20
```

**Channel attribution:**
```shopifyql
FROM sessions
SHOW referrer_source, count(sessions) AS visits, sum(converted_sessions) AS conversions
GROUP BY referrer_source
SINCE -30d UNTIL today
ORDER BY conversions DESC
```

**High-value customer segment (for Shopify Customers):**
```
amount_spent > 500 AND number_of_orders >= 3 AND last_order_date > -90d
```

**Re-engagement segment:**
```
last_order_date BETWEEN -365d AND -90d AND number_of_orders > 1
```

**Wholesale/B2B segment:**
```
customer_tags CONTAINS 'wholesale' OR amount_spent > 2000
```

---

## 5. Debugging checklist

When a query errors or returns unexpected results:

- [ ] Keyword order correct? (`FROM → SHOW → WHERE → GROUP BY → SINCE → HAVING → ORDER → LIMIT`)
- [ ] String values in single quotes (not double)?
- [ ] Filtering on a *dimension* in `WHERE`, not a metric?
- [ ] `GROUP BY` included when showing a dimension?
- [ ] Segment query doesn't have `FROM`/`SHOW` (those aren't valid in Segment QL)?
- [ ] `AND` precedence understood? (use parentheses for `OR` groups)
- [ ] Rate limit hit? (429 error → wait 60 seconds)

---

See `references/tables.md` for full lists of available dimensions and metrics per table.
