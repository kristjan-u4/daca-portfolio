/*
Roll C: Tooted + Inventuur
Baastase
*/

-- Tooted, mida ei ole kunagi müüdud.
-- Kontrollimaks, kas tegu võib olla duplikaatidega, uuritakse lisaks veel tootenimede esinemise järjekorranumbreid products tabelis.
SELECT
  p.product_id,
  p.product_name,
  p.category,
  p.subcategory,
  p.retail_price,
  s.sale_id,
  p.tootenime_esinemise_järjekorranumber
FROM (
  SELECT
  *,
  row_number() OVER (PARTITION BY product_name ORDER BY product_id) AS "tootenime_esinemise_järjekorranumber"
  FROM products
  ORDER BY product_id ASC
) p
LEFT JOIN sales s ON p.product_id = s.product_id
WHERE s.sale_id IS NULL
ORDER BY p.product_id ASC;

-- Müümata toodete koguarv. Oodatav tulemus: 12.
SELECT
  COUNT(*) AS müümata_tooteid
FROM products p
LEFT JOIN sales s ON p.product_id = s.product_id
WHERE s.sale_id IS NULL;

-- Kõige suurema kogumüügiga tooted.
SELECT
  p.product_name,
  p.category,
  p.subcategory,
  p.eco_certified,
  COUNT(s.sale_id) AS müüdud_kordi,
  SUM(s.total_price) AS kogumüük
FROM products p
INNER JOIN sales s ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name, p.category, p.subcategory, p.eco_certified
ORDER BY kogumüük DESC
LIMIT 10;

-- Toodete arv, müükide arv ja kogumüük igas tootekategoorias.
SELECT
  p.category as "kategooria",
  COUNT(DISTINCT p.product_id) AS tooteid,
  COUNT(DISTINCT CASE WHEN p.tootenime_esinemise_järjekorranumber < 2 THEN p.product_id ELSE NULL END) AS unikaalse_nimega_tooteid,
  COUNT(s.sale_id) AS müüke,
  SUM(s.total_price) AS kogumüük
FROM (
  SELECT
  *,
  row_number() OVER (PARTITION BY product_name ORDER BY product_id) AS "tootenime_esinemise_järjekorranumber"
  FROM products
  ORDER BY product_id ASC
) p
LEFT JOIN sales s ON p.product_id = s.product_id
GROUP BY p.category
ORDER BY kogumüük DESC;

-- Tabeli inventory struktuuri uurimine.
SELECT * FROM inventory LIMIT 10;

-- Uuri toodete laoseisu
SELECT * FROM (
  SELECT
    p.product_name,
    p.category,
    i.location,
    i.quantity_available,
    i.reorder_point,
    (
      CASE 
        WHEN i.product_id IS NULL THEN 'INFO PUUDUB'
        WHEN i.quantity_available <= i.reorder_point THEN 'TELLI JUURDE'
        ELSE 'OK'
      END
    ) AS staatus,
    p.tootenime_esinemise_järjekorranumber
  FROM (
    SELECT
    *,
    row_number() OVER (PARTITION BY product_name ORDER BY product_id) AS "tootenime_esinemise_järjekorranumber"
    FROM products
    ORDER BY product_id ASC
  ) p
  LEFT JOIN inventory i ON p.product_id = i.product_id
  ORDER BY i.quantity_available ASC NULLS LAST
) sq
WHERE 1 = 1
--AND sq.staatus = 'TELLI JUURDE'
AND sq.product_name = 'Kerge satiinne jakk'
;

/*
Edasijõudnute tase
*/

-- Toodete müükide ja laoseisude võrdlus.
SELECT
  p.product_name,
  p.category,
  p.retail_price,
  i.quantity_available,
  p.tootenime_esinemise_järjekorranumber,
  (p.retail_price * i.quantity_available) AS kinni_olev_raha
FROM (
    SELECT
    *,
    row_number() OVER (PARTITION BY product_name ORDER BY product_id) AS "tootenime_esinemise_järjekorranumber"
    FROM products
    ORDER BY product_id ASC
) p
LEFT JOIN sales s ON p.product_id = s.product_id
LEFT JOIN inventory i ON p.product_id = i.product_id
WHERE s.sale_id IS NULL
--AND i.quantity_available > 0
ORDER BY kinni_olev_raha DESC;