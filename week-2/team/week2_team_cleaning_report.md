# Nädala 2 meeskondlik andmekvaliteedi koondraport

**Meeskond:** Turundusanalüüsi osakond  
**Nädal:** 2  
**Adressaat:** Toomas Kask (IT-direktor)

## 1. Ülevaade leitud probleemidest
Oleme läbi viinud UrbanStyle'i nelja peamise andmedomeeni esmase diagnostika ja puhastamise. Kokku tuvastasime märkimisväärse hulga andmekvaliteedi probleeme, mis mõjutavad otseselt ärianalüüsi usaldusväärsust.

| Domeen | Probleemsete ridade arv | Peamine murekoht |
| :--- | :--- | :--- |
| **Müügiandmed** | 5509 | Suur duplikaatide hulk ja puuduvad seosed klientidega. |
| **Kliendiandmed** | 562 | Anonüümsed kliendid (puuduvad kontaktid) ja duplikaadid. |
| **Tooteandmed** | 12 | Tootenimede dubleerimine. |
| **Kvaliteedikontroll** | 1268 | Hinna ebakõlad ja mitteaktiivsed kliendid. |

---

## 2. Detailne domeenide analüüs

### 2.1. Müügiandmed
Müügiandmete tabelis tuvastasime kolm kriitilist tüüpi vigu: duplikaadid, puuduvad väärtused ja loogikavead ajas.

| Kategooria | Leitud probleeme | Kirjeldus |
| :--- | :--- | :--- |
| Duplikaadid | 4013 | Korduvad sale_id väärtused (topeltmüügid). |
| NULL customer_id | 1487 | Puuduv kliendi viide (ei saa siduda müüki kliendiga). |
| NULL sale_date | 0 | Kõik müügikuupäevad on täidetud. |
| NULL total_price | 0 | Kõik summad on täidetud. |
| Tuleviku kuupäevad | 9 | Ebaloogilised kuupäevad (hilisemad kui tänane). |

**Ärimõju:** Kõrge. Puuduvate kliendi-IDde tõttu on võimatu teha täpset kliendianalüüsi ning duplikaadid muudavad kogukäibe numbri ebausaldusväärseks.

### 2.2. Kliendiandmed
Puuduvate kontaktandmetega kliendid on süsteemis sisuliselt anonüümsed, mis takistab turundustegevust.

| Kategooria | Leitud probleeme | Kirjeldus |
| :--- | :--- | :--- |
| Duplikaatsed e-mailid | 128 | Sama e-mail on seotud mitme kliendiga. |
| NULL nimed | 0 | Ees- ja perenimed on kõigil olemas. |
| Ebajärjekindlad linnanimed | 54 | Erinevad nimekujud (nt "tallinn" vs "Tallinn"). |
| NULL telefon/e-mail | 380 | Puuduvad kontaktandmed turunduse jaoks. |

### 2.3. Tooteandmed ja Kvaliteedikontroll
Tooteanalüüsi suurimaks takistuseks on tootenimede duplikaadid. Ristvalideerimise käigus ilmnesid aga veelgi tõsisemad probleemid tabelite vahel.

| Kategooria | Leitud probleeme | Kirjeldus |
| :--- | :--- | :--- |
| Duplikaatsed tootenimed | 12 | Sama tootenimi esineb mitu korda. |
| Hinna ebakõlad | 664 | Müügihind ei klapi tootehinnaga. |
| Vaimkliendid | 592 | Kliendid, kes on süsteemis, aga pole kunagi ostnud. |
| Vaimtooted | 12 | Tooted, mida pole kordagi müüdud. |

---

## 3. Süntees ja järeldused

*   **Suurim üllatus:** Kvaliteedikontrolli käigus tuvastatud **664 hinnaerinevust** müügi- ja tootetabeli vahel ning fakt, et müügiandmete duplikaadid moonutavad oluliselt UrbanStyle'i kogukäivet.
*   **Puuduvad andmed:** Meil puudub kindlus, kas õige on tootehind või müügihind. Samuti on puudu kriitiline hulk kliendi-ID-sid ja kontaktandmeid.
*   **Soovitus Toomasele:** Hetkel ei saa andmeid äriotsuste tegemiseks usaldada. Prioriteediks peab olema **müügi- ja tooteandmete tabelite puhastamine**, alustades duplikaatide eemaldamisest ning hindade ebakõla põhjuse leidmisest.
