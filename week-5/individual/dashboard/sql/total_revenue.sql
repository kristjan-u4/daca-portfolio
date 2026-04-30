SELECT
  COALESCE(sum(s.total_price), 0) AS total_revenue
FROM sales s
WHERE s.sale_date >= :time_from
AND s.sale_date < :time_to;