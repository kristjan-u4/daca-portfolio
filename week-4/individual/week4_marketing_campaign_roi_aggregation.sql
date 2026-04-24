-- Ridade arv web_logs tabelis (peaks olema 50 000)
SELECT count(*) FROM web_logs;

-- web_logs tabeli struktuur.
SELECT * FROM web_logs LIMIT 5;

-- Erinevad turunduskanalid, ühtlustamata nimekujudega.
SELECT
  source AS turunduskanal,
  count(*) AS veebikülastuste_arv
FROM web_logs
GROUP BY source
ORDER BY veebikülastuste_arv DESC;

-- Erinevad turunduskanalid, ühtlustatud nimekujudega.
WITH web_logs_with_basic_cleaning AS (
  SELECT
    *,
    -- kõige algelisem puhastamine, tekstioperatsioonide abil:
    lower(trim(replace(source, '_', ' '))) AS sanitized_source
  FROM web_logs
),
web_logs_with_advanced_cleaning AS (
  SELECT
    *,
    -- Osad nimekujud on teise lühendid:
    (
      CASE
        WHEN sanitized_source IN ('fb') THEN 'facebook'
        WHEN sanitized_source IN ('fb ads') THEN 'facebook ads'
        WHEN sanitized_source IN ('ig') THEN 'instagram'
        WHEN sanitized_source IN ('ig ads') THEN 'instagram ads'
        ELSE sanitized_source
      END
    ) AS sanitized_source_advanced
  FROM web_logs_with_basic_cleaning
)
SELECT
  sanitized_source_advanced AS turunduskanal,
  count(*) AS veebikülastuste_arv
FROM web_logs_with_advanced_cleaning
GROUP BY sanitized_source_advanced
ORDER BY turunduskanal, veebikülastuste_arv DESC;

/*
Ühtlustame nimekujud. Koosneb mitmest sammust.
*/

-- 1. Teeme testtabeli.
DROP TABLE IF EXISTS test_web_logs;
CREATE TABLE test_web_logs (LIKE web_logs INCLUDING ALL); -- loo identne struktuur
INSERT INTO test_web_logs SELECT * FROM web_logs; -- kopeeri andmed

-- 2. Lihtsamad tekstioperatsioonid.
UPDATE test_web_logs
SET source = lower(trim(replace(source, '_', ' ')))
WHERE source <> lower(trim(replace(source, '_', ' ')));

-- 3. Lühendite ühtlustamine.
UPDATE test_web_logs
SET source = (
  CASE
    WHEN source IN ('fb') THEN 'facebook'
    WHEN source IN ('fb ads') THEN 'facebook ads'
    WHEN source IN ('ig') THEN 'instagram'
    WHEN source IN ('ig ads') THEN 'instagram ads'
    ELSE source
  END
);

-- 4. Kontrollime tulemust. Päringu tulemust saab eksportida JSON formaadis.
-- Kui ka esialgsest ühtlustamise SELECT päringust on JSON olemas, statistics
-- saab need andmed ette anda NotebookLM-ile võrdlemiseks. Kui andmed on samad,
-- siis on alust arvata, et UPDATE päringud on õigesti kirjutatud.
SELECT
  source AS turunduskanal,
  count(*) AS veebikülastuste_arv
FROM test_web_logs
GROUP BY source
ORDER BY veebikülastuste_arv DESC;

/*
Esialgse tabeli peal me UPDATE päringuid veel läbi ei vii,
sest vajalik võib olla põhjalikum analüüs. Erinevalt klientide tabeli linnanimedest,
ei sisestata tõenäoliselt turunduskanaleid inimeste poolt käsitsi, vaid seda teevad
automaatsed klikimõõtjad. Erinevustel, nagu facebook vs fb võib olla sügavam põhjus, näiteks
tarkvaraversioonierinevused. Ei saa välistada, et tulevikus võib vaja minna detailsemat analüüsi,
kus nimekujude erinevused on olulised. UPDATE päringuid esialgse tabeli peal tehes põhjustaksime
püsiva andmekao, mis muudaks sellist laadi analüüsi võimatuks.

Alljärgnevad SQL päringud teostame kõik test_web_logs tabeli peal, kus on puhastatud andmed
*/

-- Anonüümsed ja mitteanonüümsed külastajad.
WITH web_logs_with_anonymity AS (
  SELECT
    *,
    (CASE WHEN customer_id IS NULL THEN 'JAH' ELSE 'EI' END) AS anonymous
  FROM test_web_logs
)
SELECT
  w.anonymous AS anonüümne,
  count(*) AS veebikülastuste_arv
FROM web_logs_with_anonymity w
GROUP BY w.anonymous
ORDER BY veebikülastuste_arv DESC;

-- Veebikülastuste arv turunduskanali lõikes.
SELECT
  w.source AS turunduskanal,
  count(*) AS veebikülastuste_arv
FROM test_web_logs w
GROUP BY w.source
ORDER BY veebikülastuste_arv DESC;

-- Turunduskanalid, kus unikaalsete klientide arv on üle 1000.
SELECT
  w.source AS turunduskanal,
  count(DISTINCT w.customer_id) AS klientide_arv
FROM test_web_logs w
GROUP BY w.source
HAVING count(DISTINCT w.customer_id) > 1000
ORDER BY klientide_arv DESC;

/*
Võrdluseks: UrbanStyle registreeritud klientide koguarv.
See on väiksem, kui klientide arvult TOP 3 turunduskanali klientide
arvu summa. Siit järeldub, et üks klient puutub üldjuhul kokku mitme erineva turunduskanaliga.
*/
SELECT count(*) FROM customers;

/*
Klientide arv ja müük turunduskanali lõikes.
Grupitöö juhendist võetud päring. puhastatud andmete peal.
Päringus esineb müükide topeltsummeerimise probleem.
*/
SELECT
  w.source AS turunduskanal,
  COUNT(DISTINCT c.customer_id) AS kliente,
  COUNT(DISTINCT o.sale_id) AS tellimusi,
  SUM(o.total_price) AS kogukäive, -- topeltsummeerimine moonutab kogukäivet tegelikkusest palju suuremaks
  ROUND(AVG(o.total_price), 2) AS keskmine_tellimus
FROM sales o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN test_web_logs w ON c.customer_id = w.customer_id
GROUP BY w.source
ORDER BY kogukäive DESC;

-- Võrdluseks: kogukäive sales tabeli peale kokku.
SELECT sum(total_price) FROM sales;

-- Turunduskanali efektiivsus.
WITH
/*
Kuna andmemudel lubab ühel kliendil olla mitmes turunduskanalis, siis müükide
topeltsummeerimise vältimiseks summeerime müügid kõigepealt kliendi lõikes
kokku.
*/
customers_with_sales_aggregations AS (
  SELECT
    c.customer_id,
    count(s.sale_id) AS tellimusi,
    sum(s.total_price) AS kogukäive
  FROM customers c
  LEFT JOIN sales s ON c.customer_id = s.customer_id
  GROUP BY c.customer_id
),
-- Ei ole välistatud, et üks source võib esineda ühe kliendi kohta mitu korda.
-- Topeltsummeerimise ennetamiseks tuleb need kokku grupeerida:
web_logs_with_unique_sources AS (
  SELECT
    wl.source,
    wl.customer_id,
    count(*) AS veebikülastuste_arv
  FROM test_web_logs wl
  GROUP BY wl.source, wl.customer_id
),
web_logs_with_customer_aggregations AS (
  SELECT
    wl.source AS turunduskanal,
    count(*) AS klientide_arv,
    sum(c.tellimusi) AS tellimusi,
    sum(c.kogukäive) AS kogukäive
  FROM customers_with_sales_aggregations c
  LEFT JOIN web_logs_with_unique_sources wl ON c.customer_id = wl.customer_id
  GROUP BY wl.source
),
web_logs_sales_summary AS (
  SELECT
    wl.*,
    round(wl.kogukäive / wl.klientide_arv, 2) AS keskmine_tellimuse_suurus_kliendi_kohta,
    round(wl.tellimusi / wl.klientide_arv, 2) AS keskmine_tellimuste_arv_kliendi_kohta
  FROM web_logs_with_customer_aggregations wl
)
SELECT
  *,
  row_number() OVER (ORDER BY s.keskmine_tellimuse_suurus_kliendi_kohta DESC) AS koht
FROM web_logs_sales_summary s
WHERE s.turunduskanal IS NOT NULL;

-- Kampaaniate kuised trendid.
WITH
/*
Kuna andmemudel lubab ühel kliendil olla mitmes turunduskanalis, siis müükide
topeltsummeerimise vältimiseks summeerime müügid kõigepealt kliendi lõikes
kokku.
*/
customers_with_sales_aggregations AS (
  SELECT
    c.customer_id,
    date_trunc('month', s.sale_date) AS kuu, -- NULL klientide puhul, kes pole midagi ostnud
    count(s.sale_id) AS tellimuste_arv,
    sum(s.total_price) AS kogukäive
  FROM customers c
  LEFT JOIN sales s ON c.customer_id = s.customer_id
  GROUP BY c.customer_id, date_trunc('month', s.sale_date)
),
-- Ei ole välistatud, et üks source võib esineda ühe kliendi kohta mitu korda.
-- Topeltsummeerimise ennetamiseks tuleb need kokku grupeerida:
web_logs_with_unique_sources AS (
  SELECT
    wl.source,
    wl.customer_id,
    count(*) AS veebikülastuste_arv
  FROM test_web_logs wl
  GROUP BY wl.source, wl.customer_id
),
web_logs_with_customer_aggregations AS (
  SELECT
    wl.source AS turunduskanal,
    c.kuu,
    count(*) AS klientide_arv,
    sum(c.kogukäive) AS kogukäive,
    sum(c.tellimuste_arv) AS tellimuste_arv
  FROM customers_with_sales_aggregations c
  INNER JOIN web_logs_with_unique_sources wl ON c.customer_id = wl.customer_id
  GROUP BY wl.source, c.kuu
  HAVING sum(c.tellimuste_arv) > 10 -- jätame välja anomaaliatega kuud
)
SELECT
  wl.turunduskanal,
  to_char(wl.kuu, 'YYYY-MM') AS kuu,
  wl.klientide_arv,
  lag(wl.klientide_arv) OVER (ORDER BY wl.kuu) AS eelmise_kuu_klientide_arv,
  wl.klientide_arv - lag(wl.klientide_arv) OVER (ORDER BY wl.kuu) AS klientide_arvu_muutus,
  wl.kogukäive,
  wl.tellimuste_arv,
  round(wl.kogukäive / wl.klientide_arv, 2) AS kanali_efektiivsus,
  round(avg(wl.tellimuste_arv) OVER (PARTITION BY wl.turunduskanal)) AS keskmine_tellimuste_arv_kanalis_kuus
FROM web_logs_with_customer_aggregations wl
WHERE wl.turunduskanal = 'facebook ads'
ORDER BY klientide_arvu_muutus DESC NULLS LAST;

-- Kontrollpäring klientide jaoks,
-- kes pole kunagi midagi ostnud.
SELECT
  w.source,
  count(DISTINCT c.customer_id) AS klientide_arv
FROM customers c
LEFT JOIN sales s ON c.customer_id = s.customer_id
INNER JOIN test_web_logs w ON c.customer_id = w.customer_id
WHERE s.sale_id IS NULL
GROUP BY w.source
ORDER BY klientide_arv DESC;