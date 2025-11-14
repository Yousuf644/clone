-- Query to display customer purchases: customer name, product name, 
-- total quantity purchased, and total spending
-- Joins: customers -> orders -> order_items -> products

SELECT 
    c.first_name || ' ' || c.last_name AS customer_name,
    p.name AS product_name,
    SUM(oi.quantity) AS total_quantity_purchased,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) AS total_spending
FROM 
    customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    INNER JOIN products p ON oi.product_id = p.product_id
GROUP BY 
    c.customer_id,
    c.first_name,
    c.last_name,
    p.product_id,
    p.name
ORDER BY 
    customer_name,
    total_spending DESC;

