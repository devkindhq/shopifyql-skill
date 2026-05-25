# Top Products Last 30 Days

**Use case:** Identify your best-selling products by total revenue over the past 30 days.
**Tables:** `sales`
**Shopify plan:** Basic+

## Query

```shopifyql
FROM sales
SHOW product_title, product_vendor, product_type,
     net_items_sold, gross_sales, discounts, returns, net_sales, taxes, total_sales
WHERE product_title IS NOT NULL
GROUP BY product_title, product_vendor, product_type
SINCE -30d UNTIL today
ORDER BY total_sales DESC
LIMIT 20
```

## What this returns

Returns your top 20 products ranked by total sales, including a full breakdown of gross sales, discounts applied, returns, net sales, and taxes. The `net_items_sold` column shows unit volume. Use this to identify winners for restocking, featuring in marketing, or analyzing margin performance by product type.

## Variations

**Top 10 by units sold:**
```shopifyql
FROM sales
SHOW product_title, net_items_sold, total_sales
WHERE product_title IS NOT NULL
GROUP BY product_title
SINCE -30d UNTIL today
ORDER BY net_items_sold DESC
LIMIT 10
```

**Filter by product type:**
```shopifyql
FROM sales
SHOW product_title, total_sales
WHERE product_title IS NOT NULL
AND product_type = 'T-Shirts'
GROUP BY product_title
SINCE -30d UNTIL today
ORDER BY total_sales DESC
LIMIT 10
```
