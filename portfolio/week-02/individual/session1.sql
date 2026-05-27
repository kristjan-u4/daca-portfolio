-- Leia tellimused, kus klient on teadmata
SELECT sale_id, customer_id, total_price
FROM sales
WHERE customer_id IS NULL;

-- Leia kliendid, kellel ON e-mail olemas
SELECT customer_id, first_name, email
FROM customers
WHERE email IS NOT NULL;

-- Asenda puuduv kliendi nimi vaikeväärtusega
SELECT
    customer_id,
    COALESCE(first_name, 'Tundmatu') AS eesnimi,
    COALESCE(email, 'puudub@urbanstyle.ee') AS email
FROM customers;

-- Mitu asendusväärtust (valib esimese mitte-NULL väärtuse)
SELECT COALESCE(NULL, NULL, 'Kolmas valik');
-- Tulemus: 'Kolmas valik'

-- NULLIF(a, b): kui a = b, tagastab NULL; muidu tagastab a
SELECT NULLIF('', trim(' '));  -- Tulemus: NULL
SELECT NULLIF(100, 200);  -- Tulemus: 100

-- Muuda 0-hinnaga tooted NULL-iks (hind pole tegelikult 0, vaid puudub)
SELECT
    product_id,
    product_name,
    NULLIF(retail_price, 0) AS puhas_hind
FROM products;

SELECT 100 + NULL;     -- Tulemus: NULL
SELECT NULL * 5;       -- Tulemus: NULL
SELECT SUM(total_price) FROM sales;  -- SUM ignoreerib NULL-e!

-- Kuupäevade formateerimine UrbanStyle'i andmetes
SELECT
    sale_id,
    sale_date,
    TO_CHAR(sale_date, 'DD.MM.YYYY') AS eesti_kuupaev,
    TO_CHAR(sale_date, 'Day') AS nadalapäev,
    TO_CHAR(sale_date, 'YYYY-"Q"Q') AS kvartal,
    EXTRACT(DOW FROM sale_date) AS paev_nr
FROM sales
ORDER BY sale_date DESC
LIMIT 10;

-- Linnade ühtlustamise diagnostika
SELECT
    city AS originaal,
    TRIM(city) AS trimitud,
    INITCAP(TRIM(city)) AS puhastatud,
    COUNT(*) AS kliente
FROM customers
GROUP BY city
ORDER BY city;

/*
Tegelik statistika klientide päritolulinnade kohta, kus linna nimed on viidud ühtsele kujule,
eemaldatud on tühikud ning linna nimed on kõik suure algustähega.
*/
SELECT
    initcap(trim(city)) AS "linn",
    count(*) AS "kliente"
FROM customers
GROUP BY 1 -- grupeerimine esimese veeru ehk "linn" järgi SELECT osas
ORDER BY "kliente" DESC;

-- Kontrolli hinnaveeru tüüpi ja väärtusi
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
            WHEN cost_price = 0 THEN 'NULL (0 = puudub?)'
            WHEN cost_price < 0 THEN 'NEGATIIVNE!'
            ELSE 'OK'
        END AS cost_price_status,
        retail_price,
        CASE
            WHEN retail_price IS NULL THEN 'NULL'
            WHEN retail_price = 0 THEN 'NULL (0 = puudub?)'
            WHEN retail_price < 0 THEN 'NEGATIIVNE!'
            ELSE 'OK'
        END AS retail_price_status
    FROM products
    ORDER BY cost_price
) subq
GROUP BY 1, 2
ORDER BY products DESC;

-- Duplikaatide ülevaade kõigis tabelites
SELECT 'sales' AS tabel,
    COUNT(*) AS ridu_kokku,
    COUNT(DISTINCT sale_id) AS unikaalseid,
    COUNT(*) - COUNT(DISTINCT sale_id) AS duplikaate
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

-- Linnade nimed algsel kujul, kõrvutatud puhastatud kujuga ning juures klientide arvud iga formaadi jaoks.
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