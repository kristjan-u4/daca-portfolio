SELECT
  count(DISTINCT s.customer_id) AS unique_customers
FROM sales s
WHERE 1 = 1
{{filters_section}}