# Period Comparison

**Use case:** Compare current sales performance against the same period last year to measure growth.
**Tables:** `sales`
**Shopify plan:** Basic+

## Query

```shopifyql
FROM sales
SHOW net_sales, total_sales, orders_count, average_order_value
SINCE -30d UNTIL today
COMPARE TO previous_year
```

## What this returns

Returns your key sales metrics for the last 30 days alongside the same 30-day period from last year. Each metric shows both current and previous year values, making it easy to calculate year-over-year growth. This is essential for understanding whether your business is growing and by how much, while accounting for seasonal patterns.

## Variations

**Compare to previous period (sequential comparison):**
```shopifyql
FROM sales
SHOW net_sales, orders_count
SINCE -30d UNTIL today
COMPARE TO previous_period
```

**Year-over-year with day-of-week alignment:**
```shopifyql
FROM sales
SHOW net_sales, orders_count
SINCE -30d UNTIL today
COMPARE TO previous_year_match_day_of_week
```

**Monthly comparison with percent change:**
```shopifyql
FROM sales
SHOW net_sales
TIMESERIES month
SINCE -3m UNTIL today
WITH PERCENT_CHANGE
```
