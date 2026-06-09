-- Delete the copy of the customers table if it already exists:
DROP TABLE IF EXISTS customers_test;

-- Copy the customers table:
CREATE TABLE customers_test AS SELECT * FROM customers;
SELECT COUNT(*) AS row_count FROM customers_test;

-- Duplicate emails.
SELECT
  NULLIF(lower(trim(email)), '') as normalized_email,
  COUNT(*) AS copy_count
FROM customers_test
--WHERE email IS NOT NULL
GROUP BY NULLIF(lower(trim(email)), '')  -- Group by normalized form
HAVING COUNT(*) > 1
ORDER BY copy_count DESC;

-- Missing first and last names.
SELECT
    COUNT(*) FILTER (WHERE first_name IS NULL OR trim(first_name) = '') AS missing_first_name,
    COUNT(*) FILTER (WHERE last_name IS NULL OR trim(last_name) = '') AS missing_last_name
FROM customers_test;

-- Number of customers for each city name form.
SELECT city, COUNT(*) AS count
FROM customers_test
GROUP BY city
ORDER BY city;

-- Standardizing city name forms:
SELECT DISTINCT initcap(trim(city)) as "standardized_city_names" from customers_test;

-- City name forms and customer count by city.
SELECT
  subquery.normalized_city AS "standardized_city_name",
  count(*) AS "distinct_forms_count",
  sum(subquery.occurrences) as "customer_count"
FROM (
  SELECT
    city,
    initcap(trim(city)) AS normalized_city,
    count(*) AS "occurrences"
  FROM customers_test
  GROUP BY 1, 2
  ORDER BY normalized_city ASC, occurrences DESC
) subquery
GROUP BY 1
ORDER BY "distinct_forms_count" DESC, "customer_count" DESC;

-- Missing phone numbers and emails:
SELECT
    COUNT(*) FILTER (WHERE phone IS NULL OR trim(phone) = '') AS missing_phone,
    COUNT(*) FILTER (WHERE email IS NULL OR trim(email) = '') AS missing_email
FROM customers_test;

-- Replace missing first names
UPDATE customers_test
SET first_name = 'Unknown'
WHERE first_name IS NULL OR trim(first_name) = '';

-- Standardize city names using INITCAP + TRIM
UPDATE customers_test
SET city = INITCAP(TRIM(city))
WHERE city != INITCAP(TRIM(city));

-- Check the result of city name standardization
SELECT city, COUNT(*) AS count
FROM customers_test
GROUP BY city ORDER BY city;

-- Check for emails that need standardization:
SELECT * FROM customers_test
WHERE email != LOWER(TRIM(email));

-- Standardize emails to lowercase
UPDATE customers_test
SET email = LOWER(TRIM(email))
WHERE email != LOWER(TRIM(email));

-- Example: standardize phone numbers
SELECT * FROM (
  SELECT
    phone,
    CASE
        WHEN phone LIKE '+372%' THEN phone
        WHEN phone LIKE '372%' THEN '+' || phone
        WHEN LENGTH(phone) = 7 THEN '+372' || phone
        ELSE phone
    END AS standardized_phone
  FROM customers_test
  WHERE phone IS NOT NULL
) subquery
WHERE subquery.phone != subquery.standardized_phone
