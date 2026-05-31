-- 10118 rida sales tabelis:
SELECT count(*) FROM sales;

SELECT sale_date, total_price FROM sales LIMIT 5;

-- Kogukäive kuu lõikes.
SELECT
  date_trunc('month', sale_date) as kuu,
  sum(total_price) AS kogukäive
FROM sales
WHERE sale_date >= '2024-01-01'
--AND sale_date < '2025-01-01'
GROUP BY date_trunc('month', sale_date)
HAVING sum(total_price) > 120000
ORDER BY kogukäive DESC;

SELECT count(*) FROM products; -- 362 rida.
SELECT * FROM products LIMIT 5;

SELECT
  product_name,
  category,
  count(*) AS artikleid
FROM products
GROUP by product_name, category
HAVING count(*) > 1
ORDER BY artikleid DESC;

-- Kliendi nimi ja tema kogukäive.
SELECT
  c.first_name,
  c.last_name,
  sum(s.total_price) AS kogukäive
FROM customers c
LEFT JOIN sales s ON c.customer_id = s.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY kogukäive DESC NULLS LAST;

SELECT
  c.city,
  count(*) AS tellimuste_arv
FROM customers c
INNER JOIN sales s ON c.customer_id = s.customer_id
WHERE s.sale_date >= '2024-01-01'
GROUP BY c.city
HAVING count(*) > 200
ORDER BY tellimuste_arv DESC; -- ORDER BY on ressursinõudlik - kasutada ainult vajaduse korral

-- Anna periood (YYYY-MM), kuu käive ja eelmise kuu käive.
-- Näide 1: alampäring.
SELECT
  s.periood,
  s.käive,
  -- LAG on aknafunktsioon (window function), mis võtab praegusele reale eelnevalt realt s.käive väärtuse,
  -- kusjuures read on järjestatud perioodi järgi kasvavalt.
  LAG(s.käive) OVER (ORDER BY s.periood ASC) AS eelmise_kuu_käive,
  LAG(s.käive, 2) OVER (ORDER BY s.periood ASC) AS üleeelmise_kuu_käive
FROM (
  SELECT
    to_char(sale_date, 'YYYY-MM') AS periood,
    sum(total_price) AS käive
  FROM sales
  GROUP BY to_char(sale_date, 'YYYY-MM')
) s
ORDER BY s.periood;

-- Sama ülesanne.
-- Näide 2: CTE kasutamine.
WITH
  kuu_müük AS (
    SELECT
      to_char(sale_date, 'YYYY-MM') AS periood,
      sum(total_price) AS käive
    FROM sales
    GROUP BY to_char(sale_date, 'YYYY-MM')
  )
SELECT
  s.periood,
  s.käive,
  -- LAG on aknafunktsioon (window function), mis võtab praegusele reale eelnevalt realt s.käive väärtuse,
  -- kusjuures read on järjestatud perioodi järgi kasvavalt.
  LAG(s.käive) OVER (ORDER BY s.periood ASC) AS eelmise_kuu_käive,
  LAG(s.käive, 2) OVER (ORDER BY s.periood ASC) AS üleeelmise_kuu_käive
FROM kuu_müük s
ORDER BY s.periood;

-- Negatiivne arv round() teise argumendina ümardab ka täisosa.
SELECT round(123110.231, -3);