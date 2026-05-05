SELECT
  date_trunc(:interval, s.sale_date) AS interval_start,
  sum(s.total_price) AS total_revenue,
  count(s.sale_id) AS orders,
  count(DISTINCT s.customer_id) AS customers,
  avg(s.total_price) AS average_order
FROM sales s
WHERE 1 = 1
{{filters_section}}
GROUP BY date_trunc(:interval, s.sale_date)
ORDER BY interval_start ASC;