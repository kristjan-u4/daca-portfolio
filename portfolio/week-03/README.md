# Week 3: Product Sales and Inventory Analysis (Role C)

**Role:** **Role C** – Unsold Products and Inventory Analyst
**Analysis Object:** UrbanStyle.ltd product portfolio and stock levels
**Objective:** Identify "ghost products" (unsold goods), assess sales success across categories, and provide recommendations for optimizing inventory levels.

## 1. Overview and Methodology
This report focuses on combining the `products`, `sales`, and `inventory` tables. The analysis primarily used `LEFT JOIN` type relationships to identify products that do not have 
matches in the sales table. The work was carried out according to "Test, Verify, Log, Commit" methodology.

## 2. Main Findings

### 2.1. Unsold Products ("Ghost Products")
Using a `LEFT JOIN` query and filtering out records where `sale_id IS NULL`, I identified products in UrbanStyle's product range that have never been sold.

*   **Number of unsold products:** 12 products.
*   **Critical observation:** All names of unsold products are also duplicated product names in the products table. This is indicated by the product name's occurrence sequence number, 
which is 2 in all cases.

| Product ID | Product name | Category | Product Name Occurrence Sequence Number | Price (€) |
| :--- | :--- | :--- | :--- | :--- |
| 1351 | Vintage nahkne tossud | jalanõusid | 2 | 179.95 |
| 1352 | Moodne villane nahk sandaalid | jalanõusid | 2 | 368.67 |
| 1353 | Minimalistlik kashmiir bleiser | naiste_riided | 2 | 185.46 |
| 1354 | Praktiline trikoo sukkpüksid | laste_riided | 2 | 24.54 |
| 1355 | Kerge siidine nahkkindad | aksessuaarid | 2 | 219.83 |
| 1356 | Elegantne keraamiline rahakott | aksessuaarid | 2 | 155.84 |
| 1357 | Stiilne puust müts | aksessuaarid | 2 | 205.89 |
| 1358 | Luksuslik keraamiline elastne vöö | aksessuaarid | 2 | 149.55 |
| 1359 | Moodne keraamiline sall | aksessuaarid | 2 | 147.16 |
| 1360 | Stiilne orgaaniline pidžaama | laste_riided | 2 | 106.82 |
| 1361 | Klassikaline kashmiir pusa | naiste_riided | 2 | 225.81 |
| 1362 | Luksuslik teksane polo särk | meeste_riided | 2 | 347.84 |

### 2.2. TOP 10 Most Popular Products
As a result of an INNER JOIN query, UrbanStyle's bestsellers have been compiled with a sustainability label.

| Product name | Category | Subcategory | Eco certificate | Times sold | Total sales (€) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Õhuline sünteetiline sporditossud | jalanõusid | tossud | Ei | 35 | 27,347.04 |
| Trendikas goretex oxfordid | jalanõusid | kingad | Ei | 32 | 23,376.15 |
| Praktiline viskoosne jakk | naiste_riided | jakid | Ei | 35 | 22,188.80 |
| Praktiline džersii seelik | naiste_riided | seelikud | Ei | 37 | 22,039.98 |
| Boheemlaslik puuvillane tuulejope | naiste_riided | jakid | **Jah** | 30 | 21,309.96 |
| Õhuline sünteetiline kõrge kontsaga kingad | jalanõusid | kontsad | *NULL* | 38 | 21,295.56 |
| Praktiline kangast kõrge kontsaga kingad | jalanõusid | kontsad | Ei | 37 | 21,118.68 |
| Luksuslik villane pahkluu saapad | jalanõusid | botased | Ei | 28 | 19,704.87 |
| Praktiline merino villane parka | meeste_riided | jakid | Ei | 30 | 19,620.45 |
| Õhuline linane jakk | naiste_riided | jakid | Ei | 41 | 19,393.29 |

### 2.3. Number of Products, Number of Sales, and Total Sales in Euros by Product Category
Using LEFT JOIN, I examined which product categories have the largest total sales, also showing the number of sales and the number of products for comparison.

| Category | Products (by ID) | Products with unique names | Sales (count) | Total sales (€) |
| :--- | :--- | :--- | :--- | :--- |
| jalanõusid | 73 | 71 | 2,031 | 774,034.75 |
| meeste_riided | 82 | 81 | 2,266 | 749,798.72 |
| naiste_riided | 70 | 68 | 2,022 | 686,464.24 |
| aksessuaarid | 67 | 62 | 1,772 | 393,035.82 |
| laste_riided | 70 | 68 | 2,027 | 305,844.45 |

I found that the product category with the highest total sales is **jalanõusid** and the one with the lowest total sales is **laste_riided**.

### 2.4. Inventory Status and Reorder Points
By joining products with the `inventory` table, I identified goods whose stock levels have fallen below the critical threshold (`reorder_point`).

*   **Products for which inventory information is missing:** 12 products, all of which were also found to have duplicate names.
*   **Inventory needing replenishment:** 231 inventory records out of 1,400, or 16.5%, are in "REORDER" status.
*   **Most critical inventory:** **Õhuline polüester cargo püksid** in the **meeste_riided** category, with central warehouse stock being negative (-46 units). Negative stock may indicate pre-sales, but it could also be a data error.
*   **Largest inventory surplus:** **Kerge satiinne jakk** in the **naiste_riided** category, with 9,985 units in the Tartu warehouse, which is more than 250 times the critical limit.

The following table demonstrates that one product can have a very large surplus in one warehouse while simultaneously having a deficit in others.

| Product name | Category | Location | Available quantity | Reorder point | Status | Seq No. |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Sportlik merino villane ülikond | meeste_riided | ladu | 19 | 32 | **REORDER** | 1 |
| Sportlik merino villane ülikond | meeste_riided | tartu | 26 | 35 | **REORDER** | 1 |
| Sportlik merino villane ülikond | meeste_riided | tallinn | 41 | 37 | OK | 1 |
| Sportlik merino villane ülikond | meeste_riided | pärnu | **9,850** | 50 | OK | 1 |

## 3. Advanced Analysis: Capital Tied Up
I examined the inventory status of products that have never been sold. It turned out that all 12 never-sold products also lack inventory information and are products with duplicated names. The total value of unsold goods is therefore €0.

## 4. Conclusions and Recommendations

1.  **Elimination:** Products with duplicated names should be removed from the database.
2.  **Marketing Focus:** Eco-products, as their share among TOP 10 sold products is modest. Products with large inventory surplus.
3.  **Inventory Management:** The same product can have a very large surplus in one warehouse while simultaneously having a deficit in others. This indicates significant shortcomings in inventory management. Decisions on how much of each product to transport to which warehouses should be data-driven, considering sales data in addition to inventory levels.

## 5. Teamwork Reference

https://github.com/sillepragi/urbanstyle-marketing-data/blob/main/week_3/README.md
