SELECT
  COALESCE(sum(s.total_price), 0) AS total_revenue
FROM sales s
WHERE 1 = 1
{{filters_section}};