# New vs Returning Customers

**Use case:** Analyze the distribution between first-time buyers and repeat customers.
**Tables:** `sales`
**Shopify plan:** Basic+

## Query

```shopifyql
FROM sales
SHOW customer_type, net_sales, orders_count, average_order_value
GROUP BY customer_type
SINCE -30d UNTIL today
ORDER BY net_sales DESC
```

## What this returns

Returns revenue and order metrics split by customer type (new vs returning). This shows you what percentage of revenue comes from repeat customers versus new acquisition. Healthy ecommerce businesses typically see 30-50% of revenue from returning customers. Use this to evaluate retention health and balance your marketing spend between acquisition and retention.

## Variations

**Monthly trend of new vs returning:**
```shopifyql
FROM sales
SHOW customer_type, net_sales, orders_count
GROUP BY customer_type
TIMESERIES month
SINCE -6m UNTIL today
```

**First-time buyers only (for Segment QL):**
```
number_of_orders = 1 AND first_order_date > -30d
```

**Returning customers segment (for Segment QL):**
```
number_of_orders >= 2
```

**High-value repeat customers (for Segment QL):**
```
number_of_orders >= 3 AND amount_spent > 200
```
