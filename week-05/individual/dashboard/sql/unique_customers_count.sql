SELECT
  count(DISTINCT s.customer_id) AS unique_customers
FROM sales s
WHERE s.sale_date >= :time_from
AND s.sale_date < :time_to;