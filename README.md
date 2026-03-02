# ShopifyQL Skill for Claude Code

A Claude Code skill for writing, debugging, and explaining ShopifyQL analytics queries and Shopify Segment Query Language customer filters.

## What it does

Triggers automatically when you ask Claude to:
- Write a ShopifyQL report query (`FROM sales SHOW ...`)
- Build a customer segment filter
- Debug a ShopifyQL syntax error
- Translate a business question into a Shopify analytics query
- Understand available tables, dimensions, or metrics

## Covers

- **ShopifyQL** — full query structure, strict keyword ordering, all clauses (`WHERE`, `GROUP BY`, `TIMESERIES`, `HAVING`, `COMPARE TO`, `VISUALIZE`, `WITH` modifiers, semi-joins, math on metrics, `TOP N`)
- **Segment Query Language** — all attribute types, operators, date formats, and functions (`products_purchased`, `orders_placed`, `shopify_email`, `anniversary`, `customer_within_distance`, `storefront_event`)
- **Common ecommerce patterns** — top products, channel attribution, re-engagement, high-value customers, wholesale/B2B segments
- **Debugging checklist** — ordered list of the most common ShopifyQL errors

## Installation

### Claude Code

Register the marketplace and install:

```bash
/plugin marketplace add devkindhq/shopifyql-skill
/plugin install shopifyql@shopifyql-skill
```

### Manual

Clone this repo and point Claude Code at it, or copy `skills/shopifyql/SKILL.md` into your own plugin.

## License

MIT
