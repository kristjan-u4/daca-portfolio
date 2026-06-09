-- 10118 rows in the sales table:
SELECT count(*) FROM sales;

SELECT sale_date, total_price FROM sales LIMIT 5;

-- Total revenue broken down by month.
SELECT
  date_trunc('month', sale_date) as "month",
  sum(total_price) AS total_revenue
FROM sales
WHERE sale_date >= '2024-01-01'
--AND sale_date < '2025-01-01'
GROUP BY date_trunc('month', sale_date)
HAVING sum(total_price) > 120000
ORDER BY total_revenue DESC;

SELECT count(*) FROM products; -- 362 rows.
SELECT * FROM products LIMIT 5;

SELECT
  product_name,
  category,
  count(*) AS items
FROM products
GROUP by product_name, category
HAVING count(*) > 1
ORDER BY items DESC;

-- Customer name and their total revenue.
SELECT
  c.first_name,
  c.last_name,
  sum(s.total_price) AS total_revenue
FROM customers c
LEFT JOIN sales s ON c.customer_id = s.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_revenue DESC NULLS LAST;

SELECT
  c.city,
  count(*) AS order_count
FROM customers c
INNER JOIN sales s ON c.customer_id = s.customer_id
WHERE s.sale_date >= '2024-01-01'
GROUP BY c.city
HAVING count(*) > 200
ORDER BY order_count DESC; -- ORDER BY is resource-intensive - use only when necessary

-- Provide the period (YYYY-MM), monthly revenue, and previous month's revenue.
-- Example 1: Subquery.
SELECT
  s.period,
  s.revenue,
  -- LAG is a window function that retrieves the value of s.revenue from the row preceding the current row,
  -- where the rows are ordered chronologically by period.
  LAG(s.revenue) OVER (ORDER BY s.period ASC) AS previous_month_revenue,
  LAG(s.revenue, 2) OVER (ORDER BY s.period ASC) AS two_months_ago_revenue
FROM (
  SELECT
    to_char(sale_date, 'YYYY-MM') AS period,
    sum(total_price) AS revenue
  FROM sales
  GROUP BY to_char(sale_date, 'YYYY-MM')
) s
ORDER BY s.period;

-- Same task.
-- Example 2: Using a CTE (Common Table Expression).
WITH
  monthly_sales AS (
    SELECT
      to_char(sale_date, 'YYYY-MM') AS period,
      sum(total_price) AS revenue
    FROM sales
    GROUP BY to_char(sale_date, 'YYYY-MM')
  )
SELECT
  s.period,
  s.revenue,
  -- LAG is a window function that retrieves the value of s.revenue from the row preceding the current row,
  -- where the rows are ordered chronologically by period.
  LAG(s.revenue) OVER (ORDER BY s.period ASC) AS previous_month_revenue,
  LAG(s.revenue, 2) OVER (ORDER BY s.period ASC) AS two_months_ago_revenue
FROM monthly_sales s
ORDER BY s.period;

-- A negative number as the second argument in round() rounds the integer part as well.
SELECT round(123110.231, -3);