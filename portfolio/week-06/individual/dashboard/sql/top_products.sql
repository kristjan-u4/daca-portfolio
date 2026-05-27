SELECT
    p.product_name,
    sum(s.total_price) AS "total_revenue"
FROM sales s
INNER JOIN products p ON s.product_id = p.product_id
WHERE 1 = 1
{{filters_section}}
GROUP BY p.product_name
ORDER BY "total_revenue" DESC;
