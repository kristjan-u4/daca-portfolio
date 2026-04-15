# Nädal 3: Tootemüügi ja inventuuri analüüs (Roll C)

**Roll:** Roll C – Müümata toodete ja inventuuri analüütik
**Analüüsi objekt:** UrbanStyle.ltd tooteportfell ja laoseisud
**Eesmärk:** Tuvastada "vaimtooted" (müümata kaup), hinnata müügiedu kategooriate lõikes ning anda soovitused laovarude optimeerimiseks.

## 1. Ülevaade ja metodoloogia
Käesolev raport keskendub tabelite `products`, `sales` ja `inventory` ühendamisele. Analüüsis on kasutatud peamiselt `LEFT JOIN` tüüpi seoseid, et tuvastada tooted, millel puuduvad vasted müügitabelis. Töö viidi läbi vastavalt Toomas Kase "Test, Verify, Log, Commit" metoodikale.

## 2. Peamised leiud

### 2.1. Müümata tooted ("Vaimtooted")
Kasutades `LEFT JOIN` päringut ja filtreerides välja kirjed, kus `sale_id IS NULL`, tuvastasin UrbanStyle'i tootevalikust tooted, mida pole kunagi müüdud.

*   **Müümata toodete arv:** 12 toodet.
*   **Kriitiline tähelepanek:** Kõikide müümata toodete nimed on ühtlasi ka dubleeritud tootenimed products tabelis. Sellele viitab tootenime esinemise järjekorranumber, mis kõikide juhtumite puhul on 2.

| Toote ID | Toote nimi | Kategooria | Tootenime esinemise järjekorranumber | Hind (€) |
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

### 2.2. TOP 10 populaarseimat toodet
INNER JOIN päringu tulemusena on koostatud UrbanStyle'i müügihitid koos jätkusuutlikkuse märgisega.

| Toote nimi | Kategooria | Alamkategooria | Eco sertifikaat | Müüdud kordi | Kogumüük (€) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Õhuline sünteetiline sporditossud | jalanõusid | tossud | Ei | 35 | 27 347.04 |
| Trendikas goretex oxfordid | jalanõusid | kingad | Ei | 32 | 23 376.15 |
| Praktiline viskoosne jakk | naiste_riided | jakid | Ei | 35 | 22 188.80 |
| Praktiline džersii seelik | naiste_riided | seelikud | Ei | 37 | 22 039.98 |
| Boheemlaslik puuvillane tuulejope | naiste_riided | jakid | **Jah** | 30 | 21 309.96 |
| Õhuline sünteetiline kõrge kontsaga kingad | jalanõusid | kontsad | *NULL* | 38 | 21 295.56 |
| Praktiline kangast kõrge kontsaga kingad | jalanõusid | kontsad | Ei | 37 | 21 118.68 |
| Luksuslik villane pahkluu saapad | jalanõusid | botased | Ei | 28 | 19 704.87 |
| Praktiline merino villane parka | meeste_riided | jakid | Ei | 30 | 19 620.45 |
| Õhuline linane jakk | naiste_riided | jakid | Ei | 41 | 19 393.29 |

### 2.3. Toodete arv, müükide arv ja kogumüük eurodes igas tootekategoorias
LEFT JOIN abil uurisin, milliste tootekategooriate kogumüük on suurim, näidates võrdluseks ära ka müükide arvu ja toodete arvu.

| Kategooria | Tooteid (ID järgi) | Unikaalse nimega tooteid | Müüke (arv) | Kogumüük (€) |
| :--- | :--- | :--- | :--- | :--- |
| jalanõusid | 73 | 71 | 2031 | 774 034.75 |
| meeste_riided | 82 | 81 | 2266 | 749 798.72 |
| naiste_riided | 70 | 68 | 2022 | 686 464.24 |
| aksessuaarid | 67 | 62 | 1772 | 393 035.82 |
| laste_riided | 70 | 68 | 2027 | 305 844.45 |

Tuvastasin, et suurima kogumüügiga tootekategooria on jalanõud ja väikseima kogumüügiga on laste riided.

### 2.4. Inventuuri staatus ja reorder-punktid
Ühendades tooted `inventory` tabeliga, tuvastasin kauba, mille laoseis on langenud alla kriitilise piiri (`reorder_point`).

*   **Tooted, mille laoseisu kohta info puudub:** 12 toodet, mille puhul selgus ka, et kõikide nende nimed on dublikaadid.
*   **Täiendamist vajav laoseis:** 231 laoseisu kirjet 1400-st ehk 16,5% on staatuses "TELLI JUURDE".
*   **Kõige kriitilisem laoseis:** **Õhuline polüester cargo püksid** meeste_riided kategoorias, mille laoseis kesklaos on negatiivne (-46 ühikut). Negatiivne laoseis võib viidata ettemüügile, kuid tegu võib olla ka andmeveaga.
*   **Kõige suurema ülejäägiga laoseis:** **Kerge satiinne jakk** naiste_riided kategoorias, mida on Tartu laos 9985 ühikut, mis ületab rohkem kui 250 kordselt kriitilise piiri.

Alljärgnev tabel demonstreerib, et ühte toodet võib ühes laos olla kümnetes kordades üle kriitilise piiri, aga samal ajal teistes ladudes olla langenud alla selle.

| Toote nimi | Kategooria | Asukoht | Saadaval kogus | Tellimispunkt | Staatus | Jrk nr |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Sportlik merino villane ülikond | meeste_riided | ladu | 19 | 32 | **TELLI JUURDE** | 1 |
| Sportlik merino villane ülikond | meeste_riided | tartu | 26 | 35 | **TELLI JUURDE** | 1 |
| Sportlik merino villane ülikond | meeste_riided | tallinn | 41 | 37 | OK | 1 |
| Sportlik merino villane ülikond | meeste_riided | pärnu | **9850** | 50 | OK | 1 |

## 3. Edasijõudnute analüüs: Kinni olev kapital
Uurisin toodete, mida kunagi pole müüdud, laoseisu. Selgus, et kõigil 12-l mitte kunagi müüdud tootel puudub info ka laoseisu kohta ning et tegu on dubleeritud nimega toodetega. Müümata kauba väärtus on kokku seega 0€.

## 4. Järeldused ja soovitused

1.  **Likvideerimine:** Dubleeritud nimedega tooted tuleks andmebaasist eemaldada.
2.  **Turundusfookus:** Ökotooted, sest nende osakaal TOP 10 müüdud toodete hulgas on tagasihoidlik. Suure laovaru ülejäägiga tooted.
3.  **Laovarude juhtimine:** Ühel ja samal tootel võib ühes laos olla väga suur ülejääk ja samal ajal teistes ladudes puudujääk. See viitab olulistele puudujääkidele laovarude juhtimisel. Otsustamine, millistesse ladudesse kui palju mingit toodet transportida, peaks toimuma andmepõhiselt, lähtudes lisaks laoseisule ka müügiandmetest.

## 5. Meeskonnatöö viide

https://docs.google.com/document/d/1qGOioIUVrGnW9Agh-j3Dd9A8UvVJInbfLx43OtV-rqI/edit?tab=t.0
