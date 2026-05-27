# Nädal 2: SQL-andmete puhastamine (UrbanStyle.ltd)

## Ülevaade
Sel nädalal keskendusin UrbanStyle'i andmebaasi puhastamisele, et valmistada andmed ette eelseisvaks juhatuse koosolekuks. Minu roll oli **Kliendiandmete puhastaja (Roll B)**, kus minu ülesandeks oli analüüsida ja korrastada tabelit `customers`.

## Tehtud tööd
Töötasin vastavalt Toomas Kase juhistele "Test, Verify, Log, Commit" metoodika alusel:
1. **Testkeskkonna loomine:** Tegin tabelist `customers` koopia `customers_test`, et tagada turvaline andmetöötlus.
2. **Diagnostika:** Tuvastasin duplikaatsed e-mailid, puuduvad kliendinimed ja ebajärjekindlad linnanimed.
3. **Puhastamine (Edasijõudnute tase):** Ühtlustasin linnanimed (`INITCAP`, `TRIM`), normaliseerisin e-mailid ja täitsin puuduvad nimeväljad väärtusega 'Tundmatu'.

## Peamised järeldused
* **Kriitilisim leid:** Puuduvad emailid, kuna see takistab UrbanStyle’il oma klientidega suhelda ja neile kampaaniapakkumisi saata. Samuti pole anonüümsete klientide puhul selgust, kui paljud neist on samad ja kui paljud erinevad inimesed, mistõttu tekib klientide arvust moonutatud pilt.
* **Andmete seisukord:** Kliendibaas on suures osas korrektne, kuid nõuab paremat valideerimist sisestusetapis, eriti e-mailide ja asukohtade osas.
* **Soovitus:** Juurutada e-maili välja kohustuslik täitmine registreerimisel, et vältida anonüümsete kirjete teket. Linnanimede sisestamisel kasutada tekstivälja asemel rippmenüüd, et vältida erinevate nimekujude salvestamist andmebaasi.

## Failid portfoolios
* [SQL puhastamisskript](./individual/week2_customers_cleaning.sql)
* [Individuaalne puhastamisraport](./individual/week2_customers_report.md)
* [Meeskonna koondraport](./team/week2_team_cleaning_report.md)

## Enesereflektsioon (Shu-faas)
Järgisin sel nädalal täpselt etteantud juhiseid. Õppisin, kui oluline on transaktsioonide või testkoopiate kasutamine enne andmete muutmist. Suurimaks väljakutseks oli duplikaatide korrektne loendamine normaliseeritud kujul.
