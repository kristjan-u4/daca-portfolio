-- Total number of rows in the sales table.
SELECT COUNT(*) AS total_rows FROM sales;

-- Top 10 rows from the sales table.
SELECT * FROM sales
LIMIT 10;

/*
15 most recent transactions from the sales table in Tallinn,
starting from the newest.
*/
SELECT * FROM sales
WHERE store_location = 'Tallinn'
ORDER BY sale_date DESC
LIMIT 15;

-- 10 largest transactions from the sales table, starting from the largest.
SELECT * FROM sales
ORDER BY total_price DESC
LIMIT 10;

-- 10 smallest transactions from the sales table, starting from the smallest.
SELECT * FROM sales
ORDER BY total_price ASC
LIMIT 10;

-- Number of rows where customer information is missing.
SELECT
COUNT(*) - COUNT(customer_id) AS missing_customer
FROM sales;

-- All distinct sales channels in the sales table.
SELECT DISTINCT channel FROM sales;

-- Number of transactions for each store location.
SELECT
store_location,
COUNT(*) AS transactions_count
FROM sales
GROUP BY store_location
ORDER BY transactions_count DESC;

/*
All sales transactions in Tallinn with a value greater than 100 €.
The largest transactions are shown first.
*/
SELECT * FROM sales
WHERE total_price > 100
AND store_location = 'Tallinn'
ORDER BY total_price DESC;
