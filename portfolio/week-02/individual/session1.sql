-- Find orders where the customer is unknown
SELECT sale_id, customer_id, total_price
FROM sales
WHERE customer_id IS NULL;

-- Find customers who DO have an email address
SELECT customer_id, first_name, email
FROM customers
WHERE email IS NOT NULL;

-- Replace missing customer name with a default value
SELECT
    customer_id,
    COALESCE(first_name, 'Unknown') AS first_name_alias,
    COALESCE(email, 'missing@urbanstyle.ee') AS email
FROM customers;

-- Multiple default values (picks the first non-NULL value)
SELECT COALESCE(NULL, NULL, 'Third choice');
-- Result: 'Third choice'

-- NULLIF(a, b): if a = b, returns NULL; otherwise returns a
SELECT NULLIF('', trim(' '));  -- Result: NULL
SELECT NULLIF(100, 200);  -- Result: 100

-- Turn 0-price products into NULL (price is not actually 0, but missing)
SELECT
    product_id,
    product_name,
    NULLIF(retail_price, 0) AS clean_price
FROM products;

SELECT 100 + NULL;     -- Result: NULL
SELECT NULL * 5;       -- Result: NULL
SELECT SUM(total_price) FROM sales;  -- SUM ignores NULL values!

-- Date formatting in UrbanStyle data
SELECT
    sale_id,
    sale_date,
    TO_CHAR(sale_date, 'DD.MM.YYYY') AS formatted_date,
    TO_CHAR(sale_date, 'Day') AS day_of_week,
    TO_CHAR(sale_date, 'YYYY-"Q"Q') AS quarter,
    EXTRACT(DOW FROM sale_date) AS day_number
FROM sales
ORDER BY sale_date DESC
LIMIT 10;

-- Diagnostics for standardizing city names
SELECT
    city AS original,
    TRIM(city) AS trimmed,
    INITCAP(TRIM(city)) AS sanitized,
    COUNT(*) AS customers
FROM customers
GROUP BY city
ORDER BY city;

/*
Actual statistics regarding the customers' home cities, where city names have been standardized,
whitespaces removed, and all city names are capitalized.
*/
SELECT
    initcap(trim(city)) AS "city",
    count(*) AS "customers"
FROM customers
GROUP BY 1 -- grouping by the first column, i.e., "city" in the SELECT clause
ORDER BY "customers" DESC;

-- Overview of price column types and values
SELECT
    subq.cost_price_status,
    subq.retail_price_status,
    count(*) AS products
FROM (
    SELECT
        product_id,
        product_name,
        cost_price,
        CASE
            WHEN cost_price IS NULL THEN 'NULL'
            WHEN cost_price = 0 THEN 'NULL (0 = missing?)'
            WHEN cost_price < 0 THEN 'NEGATIVE!'
            ELSE 'OK'
        END AS cost_price_status,
        retail_price,
        CASE
            WHEN retail_price IS NULL THEN 'NULL'
            WHEN retail_price = 0 THEN 'NULL (0 = missing?)'
            WHEN retail_price < 0 THEN 'NEGATIVE!'
            ELSE 'OK'
        END AS retail_price_status
    FROM products
    ORDER BY cost_price
) subq
GROUP BY 1, 2
ORDER BY products DESC;

-- Overview of duplicates across all tables
SELECT 'sales' AS "table",
    COUNT(*) AS total_rows,
    COUNT(DISTINCT sale_id) AS unique_records,
    COUNT(*) - COUNT(DISTINCT sale_id) AS duplicates
FROM sales
UNION ALL
SELECT 'customers',
    COUNT(*),
    COUNT(DISTINCT email),
    COUNT(*) - COUNT(DISTINCT email)
FROM customers
UNION ALL
SELECT 'products',
    COUNT(*),
    COUNT(DISTINCT product_id),
    COUNT(*) - COUNT(DISTINCT product_id)
FROM products;

SELECT
    count(*) as "total rows",
    count(*) - count(sale_id) as "missing_sale_id",
    count(*) - count(invoice_id) as "missing_invoice_id",
    count(*) - count(customer_id) as "missing_customer_id",
    count(*) - count(product_id) as "missing_product_id"
FROM sales;

select * from products limit 2;

SELECT
    count(*) AS "total rows",
    count(*) - count(email) AS "NULL email",
    count(*) - count(phone) AS "NULL phone"
FROM customers;

-- City names in their original format, contrasted with the sanitized format, along with customer counts for each format.
SELECT
    city,
    initcap(trim(city)) as "sanitized_city",
    count(*) as "customers"
FROM customers
GROUP BY 1,2
ORDER BY "sanitized_city" ASC, "customers" DESC;

SELECT
    subq.*,
    round(subq.customers_without_email * 100.0 / subq.total_customers, 2) AS "customers_without_email_percentage"
FROM (
    SELECT
        initcap(trim(city)) AS "sanitized_city",
        count(*) AS "total_customers",
        count(*) - count(email) AS customers_without_email
    FROM customers
    GROUP BY 1
    ORDER BY "total_customers" DESC
) subq
ORDER BY "customers_without_email_percentage" DESC;