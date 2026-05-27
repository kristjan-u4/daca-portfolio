-- Tabeli sales kõikide ridade arv.
SELECT COUNT(*) AS ridade_arv FROM sales;

-- 10 esimest rida tabelist sales.
SELECT * FROM sales
LIMIT 10;

/*
15 kõige hiljutisemat Tallinna tehingut tabelist sales,
alustades uuimast.
*/
SELECT * FROM sales
WHERE store_location = 'Tallinn'
ORDER BY sale_date DESC
LIMIT 15;

-- 10 suurimat tehingut tabelist sales, alustades suurimast.
SELECT * FROM sales
ORDER BY total_price DESC
LIMIT 10;

-- 10 vähimat tehingut tabelist sales, alustades väikseimast.
SELECT * FROM sales
ORDER BY total_price ASC
LIMIT 10;

-- Ridade arv, kus puudub info kliendi kohta.
SELECT
COUNT(*) - COUNT(customer_id) AS puuduv_klient
FROM sales;

-- Kõik erinevad müügikanalid sales tabelis.
SELECT DISTINCT channel FROM sales;

-- Tehingute arv iga poe asukoha kohta.
SELECT
store_location,
COUNT(*) AS tehinguid
FROM sales
GROUP BY store_location
ORDER BY tehinguid DESC;

/*
Kõik Tallinna müügitehingud, mille väärtus on suurem kui 100 €.
Suurimad tehingud on näidatud kõigepealt.
*/
SELECT * FROM sales
WHERE total_price > 100
AND store_location = 'Tallinn'
ORDER BY total_price DESC;