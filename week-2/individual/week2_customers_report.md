# Nädala 2 individuaalne puhastamisraport: Kliendiandmed

**Roll:** Kliendiandmete puhastaja (Customer Data Cleaner)
**Objekt:** Tabel `customers` (Supabase)
**Eesmärk:** Tuvastada andmekvaliteedi probleemid (duplikaadid, NULL-väärtused, formaadivead) ja esitada ettepanekud andmete parandamiseks.

## 1. Metoodika ja turvalisus
Vastavalt IT-direktor Toomas Kase nõuetele viidi analüüs läbi **testkoopia** peal, et mitte ohustada algandmeid.
*   Loodud tabel: `customers_test`.
*   Algne ridade arv: `3150` rida.

## 2. Andmekvaliteedi koondraport

| Kategooria | Leitud probleeme | Kirjeldus |
| :--- | :--- | :--- |
| **Puuduvad e-mailid** | `380` | Kliendi email puudub või on tühi väli. |
| **Duplikaatsed e-mailid** | `128` | Sama e-mail on seotud mitme erineva kliendikirjega. |
| **NULL eesnimi** | `0` | Kliendi eesnimi puudub või on tühi väli. |
| **NULL perenimi** | `0` | Kliendi perenimi puudub või on tühi väli. |
| **Ebajärjekindlad linnanimed** | `54` | Erinevad nimekujud (nt "tallinn" vs "Tallinn"). |
| **NULL telefon/e-mail** | `0 (telefon) / 380 (email)` | Puuduvad kontaktandmed turunduse jaoks. |
| **KOKKU probleeme** | **`562`** | |

## 3. Detailne analüüs

### 3.1. Duplikaadid ja kontaktandmed
Tuvastati, et `128` e-maili aadressi korduvad andmebaasis. See viitab sellele, et osa kliente on süsteemis kirjas mitu korda, mis moonutab kliendibaasi tegelikku suurust.

### 3.2. Formaadivead ja puuduvad nimed
Linnanimede kontrollimisel selgus, et kasutusel on `54` erinevat nimekuju (nt tühikud nime alguses või erinev suurtähtede kasutus). Kontrollimisel selgus, et kõikidel klientidel on ees- ja perenimi täidetud (puuduvate nimede arv: 0).

## 4. Teostatud parandused (Edasijõudnute tase)

Vastavalt IT-direktor Toomas Kase juhistele viidi läbi andmete transformeerimine testtabelis `customers_test`. Alljärgnev tabel võrdleb andmete seisukorda enne ja pärast puhastamisprotsessi rakendamist.

| Kategooria | Enne puhastamist | Pärast puhastamist | Tegevuse kirjeldus |
| :--- | :--- | :--- | :--- |
| **Linnanimed** | 54 unikaalset nimekuju | 12 unikaalset nimekuju | Ühtlustatud suurtähed ja eemaldatud tühikud, kasutades funktsioone `INITCAP` ja `TRIM`. |
| **Kliendi nimed** | 0 puuduvat kirjet | 0 puuduvat kirjet | Kontrollitud ees- ja perenimede täidetust. NULL väärtusi ega tühje stringe ei tuvastatud. |
| **E-mailid** | 0 ebastandartset kirjet | 0 ebastandartset kirjet | Aadresside väiketähtedeks muutmise (`LOWER`) ja tühikute eemaldamise (`TRIM`) tulemusena muutusi aset ei leidnud. |
| **Telefoninumbrid** | Kõik 3150 kirjet standartsed | Kõik 3150 kirjet standartsed | `CASE WHEN` loogika ning alampäringu abil tuvastatud, et kõik olemasolevad telefoninumbrid juba vastavad standardile. |

### Puhastamise mõju ja järeldused
1. **Andmete konsistents:** Linnanimede ühtlustamine (nt "tallinn" -> "Tallinn") tagab, et edaspidine müügianalüüs asukohtade lõikes on 100% täpne ega hajuta andmeid erinevate kirjaviiside vahel.
2. **Kvaliteedi kinnitus:** Fakt, et andmebaasis puuduvad nimedeta kliendid (0 leidu), näitab, et kliendi registreerimisprotsess on selles osas toimiv, kuid nõuab jätkuvat monitoorimist.
3. **Turundusvalmidus:** Kontaktandmete kontroll kinnitas, et e-mailid ja telefoninumbrid on korrektses formaadis ning täiendavat standardiseerimist ei vajanud (0 parandust). See annab turundusmeeskonnale kindluse, et kampaaniad jõuavad adressaatideni ilma tehniliste tõrgeteta ning kinnitab olemasoleva andmesisestuse usaldusväärsust.   

## 5. Soovitus Toomasele
Kõige kriitilisem probleem on **puuduvad emailid**, kuna see moodustab andmebaasis **otsese takistuse turundustegevusele** ning takistab UrbanStyle’il oma klientidega suhelda ja neile kampaaniapakkumisi saata. Ilma kontaktandmeteta kliendid on ettevõtte jaoks "pime ala", mille tõttu on võimatu arvutada täpset **turunduse ROI-d** või koostada investorite jaoks vajalikku andmepõhist äriplaani, kuna kliendibaasi tegelik suurus ja lojaalsus on ebaselge. Soovitan juurutada andmete sisestamisel **kohustusliku e-maili välja kontrolli**, mis ei lubaks luua uut kliendikirjet ilma korrektse kontaktinfota, et vältida anonüümsete ja kasutute andmete tekkimist tulevikus.
