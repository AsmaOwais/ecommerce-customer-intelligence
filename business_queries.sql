-- Run against ecommerce_cleaned.db created in Task A.
-- Discount is fractional; returned orders are fully refunded.
-- Order counts include returns; quantity_sold excludes returns.

-- total_net_revenue
SELECT
    ROUND(
        COALESCE(
            SUM(quantity * unit_price * (1 - discount) * (1 - returned)),
            0
        ),
        2
    ) AS total_net_revenue
FROM analysis_orders;

-- top_10_customers
SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    COUNT(o.order_id) AS number_of_orders,
    ROUND(
        SUM(o.quantity * o.unit_price * (1 - o.discount) * (1 - o.returned)),
        2
    ) AS total_spending
FROM analysis_orders AS o
JOIN customers AS c
    ON o.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.city
ORDER BY total_spending DESC, c.customer_id
LIMIT 10;

-- category_revenue
SELECT
    p.category,
    ROUND(
        SUM(o.quantity * o.unit_price * (1 - o.discount) * (1 - o.returned)),
        2
    ) AS net_revenue,
    COUNT(o.order_id) AS order_count,
    SUM(o.quantity) AS quantity_ordered,
    SUM(
        CASE WHEN o.returned = 0 THEN o.quantity ELSE 0 END
    ) AS quantity_sold
FROM analysis_orders AS o
JOIN products AS p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY net_revenue DESC, p.category;

-- top_5_products
SELECT
    p.product_id,
    p.product_name,
    p.category,
    ROUND(
        SUM(o.quantity * o.unit_price * (1 - o.discount) * (1 - o.returned)),
        2
    ) AS net_revenue,
    COUNT(o.order_id) AS order_count
FROM analysis_orders AS o
JOIN products AS p
    ON o.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY net_revenue DESC, p.product_id
LIMIT 5;

