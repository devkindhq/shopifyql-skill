# Re-engagement Segment

**Use case:** Find lapsed customers who have purchased before but haven't returned in 3-12 months.
**Tables:** Shopify Customers (Segment QL)
**Shopify plan:** Basic+

## Query

```
last_order_date BETWEEN -365d AND -90d AND number_of_orders > 1
```

## What this returns

Returns customers whose most recent order was between 90 days and 1 year ago, and who have placed more than one order historically. These are proven repeat buyers who have gone dormant - prime candidates for win-back campaigns, "we miss you" emails, or special re-engagement offers. The multi-order filter ensures you're targeting customers with demonstrated loyalty, not one-time buyers.

## Variations

**Recently lapsed (30-90 days):**
```
last_order_date BETWEEN -90d AND -30d AND number_of_orders >= 2
```

**High-value lapsed customers:**
```
last_order_date BETWEEN -365d AND -90d AND amount_spent > 300
```

**Lapsed email subscribers:**
```
last_order_date BETWEEN -365d AND -90d AND email_subscription_status = 'SUBSCRIBED'
```

**At-risk customers (RFM-based, Plus):**
```
rfm_group = 'AT_RISK' AND email_subscription_status = 'SUBSCRIBED'
```
