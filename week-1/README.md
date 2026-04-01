# Nädal 1: SQL Basics -- UrbanStyle'i andmete uurimine

## Mida ma tegin

Uurisin sales tabelit SQL päringutega, keskendudes müügiandmetele. Uurimise käigus ilmnesid järgmised detailid:

* Tabelis on kokku 15234 rida ja 12 veergu.
* Veergude nimetused on: `id`, `sale_id`, `invoice_id`, `sale_date`, `customer_id`, `product_id`, `quantity`, `unit_price`, `total_price`, `channel`, `store_location`, `payment_method`.
* Tabelis on vähemalt 15 Tallinna kaupluse tehingut, millest uusim on tulevikus aset leidev tehing, mis on ajastatud 28.06.2026 peale.
* Suurim tehingusumma kõikide andmete peale kokku on 2170.40 €
* Väikseim tehingusumma kõikide andmete peale kokku on -1405.32 € ehk negatiivne.
* Tabelis sales on 1487 rida, kus puudub kliendi info ehk kus `customer_id` väli on tühi.

Pärast sales tabeli uurimist, osalesin meeskonna andmemaastiku koostamisel, kus kirjeldasin kokkuvõtlikult enda leitud olulisemaid detaile. Lisaks panustasin omalt poolt 2 tehnilist laadi soovitusega IT-direktor Toomasele:

* Kui veerus ei tohi NULL väärtusi olla, siis sellele veerule NOT NULL piirangu lisamise teel saab seda ennetada.
* Kui veerus ei tohi olla duplikaate, siis unikaalse indeksi (UNIQUE INDEX) lisamise teel sellele veerule saab duplikaatide teket ennetada.

## Peamised õppetunnid

* Puuduva väärtusega väljade ja duplikaatide teket oleks võimalik andmebaasi tasandil ennetada.

## Failid
* `individual/week1_sales_exploration.sql` -- minu SQL päringud
* `individual/week1_results_screenshot.png` -- tulemuste pilt

## Meeskonna töö

https://docs.google.com/document/d/1KF1IGFOY9RUol8cVMe5yTnogB1FGSfCGG2i4NwDDIE8/edit
