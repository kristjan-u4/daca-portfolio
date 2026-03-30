-- Päring sales tabelis, kus veerud on piiritletud:
SELECT
sale_id, customer_id, sale_date, total_price, store_location
FROM sales
limit 5;

/*
Leia 10 esimest Tartu müüki,
kus summa on mitte suurem, kui 200
 */
select *
from sales
where store_location = 'Tartu'
and total_price <= 200
order by sale_date asc -- kronoloogiliselt esimesed enne
limit 10;

-- store_location veerus esinevad erinevad väärtused:
select
distinct store_location
from sales
--where store_location is not null
order by store_location asc
limit 10;

-- store_location veerus esinevate erinevate linnade arv:
select
count(distinct store_location) as "linnade arv"
from sales;

/*
Duplikaatide uurimine sales tabelis.
*/
select
count(*) as "ridade arv",
count(distinct invoice_id) as "unikaalsete arvete arv",
count(*) - count(distinct invoice_id) as "duplikaat-arvete arv",
count(distinct sale_id) as "unikaalsete müükide arv",
count(*) - count(distinct sale_id) as "duplikaat-müükide arv"
from sales