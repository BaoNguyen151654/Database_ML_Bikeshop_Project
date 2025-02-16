WITH brand_tiers AS (
    SELECT 
        brand_id,
        AVG(list_price) as avg_price,
        CASE 
            WHEN AVG(list_price) > 1000 THEN 'high'
            WHEN AVG(list_price) >= 500 THEN 'mid'
            ELSE 'low'
        END as tier
    FROM products
    GROUP BY brand_id
),
customer_totals AS (
    SELECT 
        o.customer_id,
        SUM(oi.quantity * oi.list_price * (1 - oi.discount)) as total_spent
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.customer_id
),
latest_brand AS (
    SELECT 
        o.customer_id,
        p.brand_id
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE (o.customer_id, o.order_date) IN (
        SELECT customer_id, MAX(order_date)
        FROM orders
        GROUP BY customer_id
    )
),
most_purchased_brand AS (
    SELECT 
        o.customer_id,
        p.brand_id,
        COUNT(*) as purchase_count,
        ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY COUNT(*) DESC) as rn
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY o.customer_id, p.brand_id
)

SELECT 
    ct.customer_id,
    ct.total_spent,
    lb.brand_id as latest_purchased_brand,
    bt1.tier as latest_brand_tier,
    mpb.brand_id as most_purchased_brand,
    bt2.tier as most_purchased_brand_tier,
    b1.brand_name as latest_brand_name,
    b2.brand_name as most_purchased_brand_name
FROM customer_totals ct
LEFT JOIN latest_brand lb ON ct.customer_id = lb.customer_id
LEFT JOIN most_purchased_brand mpb ON ct.customer_id = mpb.customer_id AND mpb.rn = 1
LEFT JOIN brand_tiers bt1 ON lb.brand_id = bt1.brand_id
LEFT JOIN brand_tiers bt2 ON mpb.brand_id = bt2.brand_id
LEFT JOIN brands b1 ON lb.brand_id = b1.brand_id
LEFT JOIN brands b2 ON mpb.brand_id = b2.brand_id
ORDER BY ct.total_spent DESC;

