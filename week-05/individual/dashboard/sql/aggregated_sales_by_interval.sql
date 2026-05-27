SELECT
  date_trunc(:interval, s.sale_date) AS interval_start,
  sum(s.total_price) AS total_revenue,
  count(s.sale_id) AS orders,
  count(DISTINCT s.customer_id) AS customers
FROM sales s
WHERE s.sale_date >= :time_from
AND s.sale_date < :time_to
GROUP BY date_trunc(:interval, s.sale_date)
ORDER BY interval_start ASC;