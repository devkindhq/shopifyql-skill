# Revenue by Channel

**Use case:** Break down your sales performance across different sales channels (Online Store, POS, Shop app, etc.).
**Tables:** `sales`
**Shopify plan:** Basic+

## Query

```shopifyql
FROM sales
SHOW sales_channel, gross_sales, discounts, net_sales, orders_count, average_order_value
GROUP BY sales_channel
SINCE -30d UNTIL today
ORDER BY net_sales DESC
```

## What this returns

Returns each sales channel with its revenue metrics: gross sales before discounts, total discounts given, net sales after discounts, order count, and average order value. Use this to understand which channels drive the most revenue and which have the healthiest AOV. Channels typically include Online Store, Point of Sale, Shop app, Buy Button, and any third-party channels you've connected.

## Variations

**Monthly trend by channel:**
```shopifyql
FROM sales
SHOW sales_channel, net_sales
GROUP BY sales_channel
TIMESERIES month
SINCE -6m UNTIL today
```

**Channel performance for a specific product:**
```shopifyql
FROM sales
SHOW sales_channel, net_sales, net_items_sold
WHERE product_title = 'Classic T-Shirt'
GROUP BY sales_channel
SINCE -30d UNTIL today
ORDER BY net_sales DESC
```
