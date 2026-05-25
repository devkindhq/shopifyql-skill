# Traffic by Source

**Use case:** See where your website visitors are coming from and which sources drive the most traffic.
**Tables:** `sessions`
**Shopify plan:** Basic+

## Query

```shopifyql
FROM sessions
SHOW referrer_source, sessions_count, converted_sessions
GROUP BY referrer_source
SINCE -30d UNTIL today
ORDER BY sessions_count DESC
```

## What this returns

Returns each traffic source (Google, Facebook, Direct, Email, etc.) with the total number of sessions and how many of those sessions resulted in a purchase. This helps you understand which marketing channels drive the most traffic and which have the highest quality visitors. Compare `converted_sessions` to `sessions_count` to calculate conversion rate by source.

## Variations

**Include bounce and engagement metrics:**
```shopifyql
FROM sessions
SHOW referrer_source, sessions_count, converted_sessions, bounced_sessions
GROUP BY referrer_source
SINCE -30d UNTIL today
ORDER BY sessions_count DESC
LIMIT 20
```

**Traffic trend over time:**
```shopifyql
FROM sessions
SHOW referrer_source, sessions_count
GROUP BY referrer_source
TIMESERIES week
SINCE -3m UNTIL today
```

**Filter to paid sources only:**
```shopifyql
FROM sessions
SHOW referrer_source, sessions_count, converted_sessions
WHERE referrer_source = 'google'
OR referrer_source = 'facebook'
GROUP BY referrer_source
SINCE -30d UNTIL today
```
