# High-Value Customers

**Use case:** Create a segment of your most valuable customers based on spend and order frequency.
**Tables:** Shopify Customers (Segment QL)
**Shopify plan:** Basic+

## Query

```
amount_spent > 500 AND number_of_orders >= 3 AND last_order_date > -90d
```

## What this returns

Returns customers who have spent more than $500 total, placed at least 3 orders, and have purchased within the last 90 days. This segment represents your active high-value customers - the people most worth nurturing with VIP treatment, early access to products, or exclusive offers. Use this in the Shopify Admin customer segment builder or via the Customers API.

## Variations

**VIP tier (top spenders):**
```
amount_spent > 1000 AND number_of_orders >= 5
```

**High-value subscribers:**
```
amount_spent > 500 AND email_subscription_status = 'SUBSCRIBED'
```

**High-value in specific region:**
```
amount_spent > 500 AND customer_countries CONTAINS 'US'
```

**Using predictive analytics (Plus):**
```
predicted_spend_tier = 'HIGH' AND last_order_date > -30d
```
