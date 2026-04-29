SELECT
  date_trunc(:interval, s.sale_date) AS perioodi_algus,
  sum(s.total_price) AS käive,
  count(s.sale_id) AS tellimusi,
  count(DISTINCT s.customer_id) AS kliente
FROM sales s
WHERE s.sale_date >= :time_from
AND s.sale_date < :time_to
GROUP BY date_trunc(:interval, s.sale_date)
ORDER BY perioodi_algus ASC;