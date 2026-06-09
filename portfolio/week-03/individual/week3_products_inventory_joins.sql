/*
Role C: Products + Inventory
Basic Level
*/

-- Products that have never been sold.
-- To check if these might be duplicates, the occurrence rank of product names in the products table is also examined.
SELECT
  p.product_id,
  p.product_name,
  p.category,
  p.subcategory,
  p.retail_price,
  s.sale_id,
  p.product_name_occurrence_rank
FROM (
  SELECT
  *,
  row_number() OVER (PARTITION BY product_name ORDER BY product_id) AS "product_name_occurrence_rank"
  FROM products
  ORDER BY product_id ASC
) p
LEFT JOIN sales s ON p.product_id = s.product_id
WHERE s.sale_id IS NULL
ORDER BY p.product_id ASC;

-- Total number of unsold products. Expected result: 12.
SELECT
  COUNT(*) AS unsold_products
FROM products p
LEFT JOIN sales s ON p.product_id = s.product_id
WHERE s.sale_id IS NULL;

-- Products with the highest total sales.
SELECT
  p.product_name,
  p.category,
  p.subcategory,
  p.eco_certified,
  COUNT(s.sale_id) AS times_sold,
  SUM(s.total_price) AS total_sales
FROM products p
INNER JOIN sales s ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name, p.category, p.subcategory, p.eco_certified
ORDER BY total_sales DESC
LIMIT 10;

-- Number of products, number of sales, and total sales in each product category.
SELECT
  p.category AS category,
  COUNT(DISTINCT p.product_id) AS products,
  COUNT(DISTINCT CASE WHEN p.product_name_occurrence_rank < 2 THEN p.product_id ELSE NULL END) AS products_with_unique_names,
  COUNT(s.sale_id) AS sales,
  SUM(s.total_price) AS total_sales
FROM (
  SELECT
  *,
  row_number() OVER (PARTITION BY product_name ORDER BY product_id) AS "product_name_occurrence_rank"
  FROM products
  ORDER BY product_id ASC
) p
LEFT JOIN sales s ON p.product_id = s.product_id
GROUP BY p.category
ORDER BY total_sales DESC;

-- Examine the structure of the inventory table.
SELECT * FROM inventory LIMIT 10;

-- Examine product stock status
SELECT * FROM (
  SELECT
    p.product_name,
    p.category,
    i.location,
    i.quantity_available,
    i.reorder_point,
    (
      CASE 
        WHEN i.product_id IS NULL THEN 'INFO MISSING'
        WHEN i.quantity_available <= i.reorder_point THEN 'REORDER'
        ELSE 'OK'
      END
    ) AS status,
    p.product_name_occurrence_rank
  FROM (
    SELECT
    *,
    row_number() OVER (PARTITION BY product_name ORDER BY product_id) AS "product_name_occurrence_rank"
    FROM products
    ORDER BY product_id ASC
  ) p
  LEFT JOIN inventory i ON p.product_id = i.product_id
  ORDER BY i.quantity_available ASC NULLS LAST
) subquery
WHERE 1 = 1
--AND subquery.status = 'REORDER'
AND subquery.product_name = 'Kerge satiinne jakk'
;

/*
Advanced Level
*/

-- Comparison of product sales and inventory levels.
SELECT
  p.product_name,
  p.category,
  p.retail_price,
  i.quantity_available,
  p.product_name_occurrence_rank,
  (p.retail_price * i.quantity_available) AS capital_tied_up
FROM (
    SELECT
    *,
    row_number() OVER (PARTITION BY product_name ORDER BY product_id) AS "product_name_occurrence_rank"
    FROM products
    ORDER BY product_id ASC
) p
LEFT JOIN sales s ON p.product_id = s.product_id
LEFT JOIN inventory i ON p.product_id = i.product_id
WHERE s.sale_id IS NULL
--AND i.quantity_available > 0
ORDER BY capital_tied_up DESC;
