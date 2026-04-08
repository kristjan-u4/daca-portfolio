-- Duplikaatsed emailid.
SELECT
  lower(trim(email)) as normaliseeritud_email,
  COUNT(*) AS koopiate_arv
FROM customers_test
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY koopiate_arv DESC;

-- Puuduvad ees- ja perekonnanimed.
SELECT
    COUNT(*) FILTER (WHERE first_name IS NULL OR trim(first_name) = '') AS puuduv_eesnimi,
    COUNT(*) FILTER (WHERE last_name IS NULL OR trim(last_name) = '') AS puuduv_perenimi
FROM customers_test;

-- Klientide arv iga linna nimekuju kohta.
SELECT city, COUNT(*) AS arv
FROM customers_test
GROUP BY city
ORDER BY city;

-- Linnade nimekujude ühtlustamine:
SELECT DISTINCT initcap(trim(city)) as "linnade ühtlustatud nimekujud" from customers_test;

-- Linnade nimekujude ja klientide arv linnade lõikes.
SELECT
  sq.normalized_city AS "ühtlustatud linnanimi",
  count(*) AS "erinevate nimekujude arv",
  sum(sq.occurrences) as "klientide arv"
FROM (
  SELECT
    city,
    initcap(trim(city)) AS normalized_city,
    count(*) AS "occurrences"
  FROM customers_test
  GROUP BY 1, 2
  ORDER BY normalized_city ASC, occurrences DESC
) sq
GROUP BY 1
ORDER BY "erinevate nimekujude arv" DESC, "klientide arv" DESC;

-- Puuduvad telefoninumbrid ja emailid:
SELECT
    COUNT(*) FILTER (WHERE phone IS NULL OR trim(phone) = '') AS puuduv_telefon,
    COUNT(*) FILTER (WHERE email IS NULL OR trim(email) = '') AS puuduv_email
FROM customers_test;

-- Asenda puuduvad eesnimed
UPDATE customers_test
SET first_name = 'Tundmatu'
WHERE first_name IS NULL OR trim(first_name) = '';

-- Ühtlusta linnanimed INITCAP + TRIM abil
UPDATE customers_test
SET city = INITCAP(TRIM(city))
WHERE city != INITCAP(TRIM(city));

-- Kontrolli linnanimede ühtlustamise tulemust
SELECT city, COUNT(*) AS arv
FROM customers_test
GROUP BY city ORDER BY city;

-- Kontrolli, kas leidub standardiseerimist vajavaid emaile:
SELECT * FROM customers_test
WHERE email != LOWER(TRIM(email));

-- Standardiseeri e-mailid väiketähtedeks
UPDATE customers_test
SET email = LOWER(TRIM(email))
WHERE email != LOWER(TRIM(email));

-- Näide: standardiseeri telefoninumbrid
SELECT * FROM (
  SELECT
    phone,
    CASE
        WHEN phone LIKE '+372%' THEN phone
        WHEN phone LIKE '372%' THEN '+' || phone
        WHEN LENGTH(phone) = 7 THEN '+372' || phone
        ELSE phone
    END AS standardne_telefon
  FROM customers_test
  WHERE phone IS NOT NULL
) sq
WHERE sq.phone != sq.standardne_telefon