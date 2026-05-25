# Conversion Rate

**Use case:** Track your store's session-to-order conversion rate over time.
**Tables:** `sessions`
**Shopify plan:** Basic+

## Query

```shopifyql
FROM sessions
SHOW sessions_count, converted_sessions
TIMESERIES day
SINCE -30d UNTIL today
```

## What this returns

Returns daily session counts alongside converted sessions (sessions that resulted in a purchase). To calculate conversion rate, divide `converted_sessions` by `sessions_count`. Typical ecommerce conversion rates range from 1-4%. Track this over time to spot trends and measure the impact of site changes, promotions, or seasonality on purchase behavior.

## Variations

**Weekly conversion trend:**
```shopifyql
FROM sessions
SHOW sessions_count, converted_sessions
TIMESERIES week
SINCE -3m UNTIL today
```

**Conversion by device type:**
```shopifyql
FROM sessions
SHOW device_type, sessions_count, converted_sessions
GROUP BY device_type
SINCE -30d UNTIL today
```

**Conversion by landing page:**
```shopifyql
FROM sessions
SHOW landing_page_path, sessions_count, converted_sessions
GROUP BY landing_page_path
SINCE -30d UNTIL today
ORDER BY sessions_count DESC
LIMIT 20
```

**Conversion by country:**
```shopifyql
FROM sessions
SHOW visitor_country, sessions_count, converted_sessions
GROUP BY visitor_country
SINCE -30d UNTIL today
ORDER BY sessions_count DESC
LIMIT 15
```
