SELECT
  COALESCE(sum(s.total_price), 0.0) AS total_revenue,
  count(s.sale_id) AS orders,
  count(DISTINCT s.customer_id) AS customers,
  COALESCE(round(avg(s.total_price), 2), 0.0) AS average_order
FROM sales s
WHERE 1 = 1
{{filters_section}};