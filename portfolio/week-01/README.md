# Week 1: SQL Basics -- Exploring UrbanStyle's Data

## What I Did

I explored the `sales` table with SQL queries, focusing on sales data. During the exploration, the following details emerged:

*   The table contains a total of 15,234 rows and 12 columns.
*   Column names are: `id`, `sale_id`, `invoice_id`, `sale_date`, `customer_id`, `product_id`, `quantity`, `unit_price`, `total_price`, `channel`, `store_location`, `payment_method`.
*   The table contains at least 15 transactions for the Tallinn store, the newest of which is a future transaction scheduled for 28.06.2026.
*   The largest transaction amount across all data is €2170.40.
*   The smallest transaction amount across all data is -€1405.32, which is negative.
*   The `sales` table has 1487 rows where customer information is missing, i.e., where the `customer_id` field is empty.

After examining the `sales` table, I participated in compiling the team's data landscape, where I briefly described the most important details I found. Additionally, I contributed 2 technical recommendations to IT Director Toomas:

*   If a column should not contain NULL values, this can be prevented by adding a NOT NULL constraint to that column.
*   If a column should not contain duplicates, the creation of duplicates can be prevented by adding a unique index (UNIQUE INDEX) to that column.

## Key Lessons Learned

*   The creation of missing value fields and duplicates could be prevented at the database level.

## Files
*   [My SQL Queries](./individual/week1_sales_exploration.sql)
*   [Screenshot of Query Results](./individual/week1_results_screenshot.png)

## Team Work

https://github.com/sillepragi/urbanstyle-marketing-data/blob/main/week_1/README.md
