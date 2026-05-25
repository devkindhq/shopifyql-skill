# Low Stock Alert

**Use case:** Identify products running low on inventory that need restocking.
**Tables:** `inventory`
**Shopify plan:** Basic+

## Query

```shopifyql
FROM inventory
SHOW product_title, variant_title, inventory_quantity, inventory_location
WHERE inventory_quantity > 0
AND inventory_quantity <= 10
GROUP BY product_title, variant_title, inventory_location
ORDER BY inventory_quantity ASC
LIMIT 50
```

## What this returns

Returns products and variants with stock levels between 1 and 10 units, sorted by lowest stock first. Each row shows the product name, variant (size/color), current quantity, and location. Use this for daily/weekly inventory reviews to identify items needing reorders before they sell out. Adjust the threshold (10) based on your typical sales velocity.

## Variations

**Out of stock items:**
```shopifyql
FROM inventory
SHOW product_title, variant_title, inventory_location
WHERE inventory_quantity = 0
GROUP BY product_title, variant_title, inventory_location
LIMIT 100
```

**Low stock by location:**
```shopifyql
FROM inventory
SHOW inventory_location, product_title, inventory_quantity
WHERE inventory_quantity <= 5
AND inventory_quantity > 0
GROUP BY inventory_location, product_title
ORDER BY inventory_location ASC, inventory_quantity ASC
```

**High-value items running low (combine with sales data):**
```shopifyql
FROM inventory
SHOW product_title, variant_sku, inventory_quantity
WHERE inventory_quantity <= 10
AND inventory_quantity > 0
GROUP BY product_title, variant_sku
ORDER BY inventory_quantity ASC
LIMIT 25
```
