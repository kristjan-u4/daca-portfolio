# DACA Portfolio -- Kristjan

## About Me
I have worked as a software developer (Ruby, Java) for many years, but now I am looking to make a career pivot into the field of data analytics.

## Goal
To learn data analytics -- SQL, Python, visualization -- and build a professional portfolio.

## Portfolio

Weekly projects are located in the [portfolio](./portfolio) directory.

### Week by Week

| Week | Start | End | Topic | Summary | Status |
|------|-------|-----|-------|---------|--------|
| 0 | 23 Mar 2026 | 29 Mar 2026 | [Onboarding](./portfolio/week-00) | Setting up software (VS Code, Python & packages) and services (GitHub repository, Supabase, NotebookLM) needed for work. | Completed |
| 1 | 30 Mar 2026 | 05 Apr 2026 | [SQL Basics](./portfolio/week-01) | Reading data (`SELECT`), filtering (`WHERE`, `AND`, `OR`), sorting (`ORDER BY`), `NULL` keyword, counting(`count(*)`, `count(column_name)`, `count(DISTINCT column_name)`). Exploring `sales` table (**15,234** rows x **12** columns). | Completed |
| 2 | 06 Apr 2026 | 12 Apr 2026 | [SQL Cleaning](./portfolio/week-02) | Detecting duplicate values using `GROUP BY` + `HAVING` and duplicate rows using `row_number()`. Using `trim()`, `lower()`, `initcap()` to unify different forms of text values (e.g. out of **54** distinct forms in `customers.city` column, it was discovered that there were only **12** unique cities). Creating a copy from a table (e.g. `customers_test` based on `customers`) to perform `UPDATE` and `DELETE` safely without modifying original data, since SQL write operations are irreversible. Using `UPDATE` to sanitize data and `DELETE` to remove duplicates. Writing a markdown report about data cleaning process and its results. | Completed |
| 3 | 13 Apr 2026 | 19 Apr 2026 | [SQL JOINs](./portfolio/week-03) | Using `INNER JOIN`, `LEFT JOIN`, and occasionally `RIGHT JOIN` - to combine tables by matching primary and foreign keys. Joining `products` table with `sales` and `inventory` tables using `LEFT JOIN` in order to analyse products - including those without inventory and sales. Noticed anomalies regarding product quantities in different inventory locations (e.g. a product has **9,850** items in Pärnu which is more than **260** times over reorder point (**37**), while in other cities the number of product items is only slightly above or even below the reorder point). | Completed |
| 4 | 20 Apr 2026 | 26 Apr 2026 | [SQL Aggregation](./portfolio/week-04) | | Completed |
| 5 | 27 Apr 2026 | 03 May 2026 | [Visualization - Design](./portfolio/week-05) | | Completed |
| 6 | 04 May 2026 | 10 May 2026 | [Visualization - Data](./portfolio/week-06) | | Completed |
| 7 | 11 May 2026 | 17 May 2026 | [Python - Pandas](./portfolio/week-07) | | Completed |
| 8 | 18 May 2026 | 24 May 2026 | [Python - APIs](./portfolio/week-08) | | Completed |
| 9 | 25 May 2026 | 31 May 2026 | [Career Preparation](./portfolio/week-09) | | Completed |
| 10 | 01 Jun 2026 | 10 Jun 2026 | [Portfolio Defense](./portfolio/week-10) | | In Progress |
