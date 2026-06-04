-- Number of rows in the web_logs table (should be 50,000)
SELECT count(*) FROM web_logs;

-- Structure of the web_logs table.
SELECT * FROM web_logs LIMIT 5;

-- Various marketing channels, with unstandardized names.
SELECT
  source AS marketing_channel,
  count(*) AS web_visits_count
FROM web_logs
GROUP BY source
ORDER BY web_visits_count DESC;

-- Various marketing channels, with standardized names.
WITH web_logs_with_basic_cleaning AS (
  SELECT
    *,
    -- The most basic cleaning, using text operations:
    lower(trim(replace(source, '_', ' '))) AS sanitized_source
  FROM web_logs
),
web_logs_with_advanced_cleaning AS (
  SELECT
    *,
    -- Some names are abbreviations of others:
    (
      CASE
        WHEN sanitized_source IN ('fb') THEN 'facebook'
        WHEN sanitized_source IN ('fb ads') THEN 'facebook ads'
        WHEN sanitized_source IN ('ig') THEN 'instagram'
        WHEN sanitized_source IN ('ig ads') THEN 'instagram ads'
        ELSE sanitized_source
      END
    ) AS sanitized_source_advanced
  FROM web_logs_with_basic_cleaning
)
SELECT
  sanitized_source_advanced AS marketing_channel,
  count(*) AS web_visits_count
FROM web_logs_with_advanced_cleaning
GROUP BY sanitized_source_advanced
ORDER BY marketing_channel, web_visits_count DESC;

/*
Standardize the naming conventions. Consists of several steps.
*/

-- 1. Create a test table.
DROP TABLE IF EXISTS test_web_logs;
CREATE TABLE test_web_logs (LIKE web_logs INCLUDING ALL); -- create identical structure
INSERT INTO test_web_logs SELECT * FROM web_logs; -- copy data

-- 2. Simpler text operations.
UPDATE test_web_logs
SET source = lower(trim(replace(source, '_', ' ')))
WHERE source <> lower(trim(replace(source, '_', ' ')));

-- 3. Standardize abbreviations.
UPDATE test_web_logs
SET source = (
  CASE
    WHEN source IN ('fb') THEN 'facebook'
    WHEN source IN ('fb ads') THEN 'facebook ads'
    WHEN source IN ('ig') THEN 'instagram'
    WHEN source IN ('ig ads') THEN 'instagram ads'
    ELSE source
  END
);

-- 4. Check the result. The query result can be exported in JSON format.
-- If JSON from the initial standardization SELECT query is also available, statistics
-- can provide this data to NotebookLM for comparison. If the data is the same,
-- then there is reason to believe that the UPDATE queries are written correctly.
SELECT
  source AS marketing_channel,
  count(*) AS web_visits_count
FROM test_web_logs
GROUP BY source
ORDER BY web_visits_count DESC;

/*
We are not yet performing UPDATE queries on the original table,
because more thorough analysis may be necessary. Unlike city names in the customer table,
marketing channels are probably not entered manually by people, but by
automatic click trackers. Differences, such as facebook vs fb, may have a deeper reason, for example,
software version differences. It cannot be ruled out that in the future, a more detailed analysis may be needed,
where differences in naming conventions are important. Performing UPDATE queries on the original table would cause
permanent data loss, which would make such an analysis impossible.

All subsequent SQL queries will be performed on the test_web_logs table, which contains cleaned data
*/

-- Anonymous and non-anonymous visitors.
WITH web_logs_with_anonymity AS (
  SELECT
    *,
    (CASE WHEN customer_id IS NULL THEN 'YES' ELSE 'NO' END) AS is_anonymous
  FROM test_web_logs
)
SELECT
  w.is_anonymous AS is_anonymous,
  count(*) AS web_visits_count
FROM web_logs_with_anonymity w
GROUP BY w.is_anonymous
ORDER BY web_visits_count DESC;

-- Number of web visits by marketing channel.
SELECT
  w.source AS marketing_channel,
  count(*) AS web_visits_count
FROM test_web_logs w
GROUP BY w.source
ORDER BY web_visits_count DESC;

-- Marketing channels where the number of unique customers is over 1000.
SELECT
  w.source AS marketing_channel,
  count(DISTINCT w.customer_id) AS customer_count
FROM test_web_logs w
GROUP BY w.source
HAVING count(DISTINCT w.customer_id) > 1000
ORDER BY customer_count DESC;

/*
For comparison: Total number of registered UrbanStyle customers.
This is smaller than the sum of customer counts for the TOP 3 marketing channels.
From this, it can be concluded that a single customer generally interacts with multiple different marketing channels.
*/
SELECT count(*) FROM customers;

/*
Customer count and sales by marketing channel.
Query taken from the group work guide. On cleaned data.
The query has a problem with double summing of sales.
*/
SELECT
  w.source AS marketing_channel,
  COUNT(DISTINCT c.customer_id) AS customer_count,
  COUNT(DISTINCT o.sale_id) AS orders_count,
  SUM(o.total_price) AS total_revenue, -- double summing distorts total revenue to be much larger than reality
  ROUND(AVG(o.total_price), 2) AS average_order_value
FROM sales o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN test_web_logs w ON c.customer_id = w.customer_id
GROUP BY w.source
ORDER BY total_revenue DESC;

-- For comparison: total revenue across the sales table.
SELECT sum(total_price) FROM sales;

-- Marketing channel efficiency.
WITH
/*
Since the data model allows one customer to be in multiple marketing channels,
to avoid double-summing sales, we first sum sales at the customer level.
*/
customers_with_sales_aggregations AS (
  SELECT
    c.customer_id,
    count(s.sale_id) AS orders_count,
    sum(s.total_price) AS total_revenue
  FROM customers c
  LEFT JOIN sales s ON c.customer_id = s.customer_id
  GROUP BY c.customer_id
),
-- It's not impossible that a single source might appear multiple times for one customer.
-- To prevent double-summing, these must be grouped together:
web_logs_with_unique_sources AS (
  SELECT
    wl.source,
    wl.customer_id,
    count(*) AS web_visits_count
  FROM test_web_logs wl
  GROUP BY wl.source, wl.customer_id
),
web_logs_with_customer_aggregations AS (
  SELECT
    wl.source AS marketing_channel,
    count(*) AS customer_count,
    sum(c.orders_count) AS orders_count,
    sum(c.total_revenue) AS total_revenue
  FROM customers_with_sales_aggregations c
  LEFT JOIN web_logs_with_unique_sources wl ON c.customer_id = wl.customer_id
  GROUP BY wl.source
),
web_logs_sales_summary AS (
  SELECT
    wl.*,
    round(wl.total_revenue / wl.customer_count, 2) AS avg_order_size_per_customer,
    round(wl.orders_count / wl.customer_count, 2) AS avg_orders_per_customer
  FROM web_logs_with_customer_aggregations wl
)
SELECT
  *,
  row_number() OVER (ORDER BY s.avg_order_size_per_customer DESC) AS rank
FROM web_logs_sales_summary s
WHERE s.marketing_channel IS NOT NULL;

-- Monthly campaign trends.
WITH
/*
Since the data model allows one customer to be in multiple marketing channels,
to avoid double-summing sales, we first sum sales at the customer level.
*/
customers_with_sales_aggregations AS (
  SELECT
    c.customer_id,
    date_trunc('month', s.sale_date) AS month, -- For NULL customers who haven't bought anything
    count(s.sale_id) AS orders_count,
    sum(s.total_price) AS total_revenue
  FROM customers c
  LEFT JOIN sales s ON c.customer_id = s.customer_id
  GROUP BY c.customer_id, date_trunc('month', s.sale_date)
),
-- It's not impossible that a single source might appear multiple times for one customer.
-- To prevent double-summing, these must be grouped together:
web_logs_with_unique_sources AS (
  SELECT
    wl.source,
    wl.customer_id,
    count(*) AS web_visits_count
  FROM test_web_logs wl
  GROUP BY wl.source, wl.customer_id
),
web_logs_with_customer_aggregations AS (
  SELECT
    wl.source AS marketing_channel,
    c.month,
    count(*) AS customer_count,
    sum(c.total_revenue) AS total_revenue,
    sum(c.orders_count) AS orders_count
  FROM customers_with_sales_aggregations c
  INNER JOIN web_logs_with_unique_sources wl ON c.customer_id = wl.customer_id
  GROUP BY wl.source, c.month
  HAVING sum(c.orders_count) > 10 -- Exclude months with anomalies
)
SELECT
  wl.marketing_channel,
  to_char(wl.month, 'YYYY-MM') AS month,
  wl.customer_count,
  lag(wl.customer_count) OVER (ORDER BY wl.month) AS previous_month_customer_count,
  wl.customer_count - lag(wl.customer_count) OVER (ORDER BY wl.month) AS customer_count_change,
  wl.total_revenue,
  wl.orders_count,
  round(wl.total_revenue / wl.customer_count, 2) AS channel_efficiency,
  round(avg(wl.orders_count) OVER (PARTITION BY wl.marketing_channel)) AS avg_monthly_orders_per_channel
FROM web_logs_with_customer_aggregations wl
WHERE wl.marketing_channel = 'facebook ads'
ORDER BY customer_count_change DESC NULLS LAST;

-- Control query for customers
-- who have never made a purchase.
SELECT
  w.source,
  count(DISTINCT c.customer_id) AS customer_count
FROM customers c
LEFT JOIN sales s ON c.customer_id = s.customer_id
INNER JOIN test_web_logs w ON c.customer_id = w.customer_id
WHERE s.sale_id IS NULL
GROUP BY w.source
ORDER BY customer_count DESC;
