SELECT
    c.city,
    sum(s.total_price) AS total_revenue
FROM sales s
INNER JOIN customers c ON s.customer_id = c.customer_id
WHERE 1 = 1
{{filters_section}}
GROUP BY c.city
ORDER BY total_revenue DESC;