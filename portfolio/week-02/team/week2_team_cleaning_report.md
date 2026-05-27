# MEESKOND: Turundusanalüüsi osakond | NÄDAL: 2 | TEGELANE: Toomas Kask

## ANDMEKVALITEEDI KOONDRAPORT

### PEAMISED LEIUD:

#### 1. Müügiandmed
Leitud **5509** probleemset rida — see tähendab äriliselt, et leitud on 3 tüüpi andmekvaliteedi probleemi - duplikaadid, puuduvad väärtused, loogikaviga ajas, mis vajavad täpsemat kontrollimist!

| **Kategooria** | **Leitud probleeme** | **Kirjeldus** |
| :--- | :--- | :--- |
| Duplikaadid | 4013 | Korduvad saleid väärtused |
| NULL customerid | 1487 | Puuduv kliendi viide |
| NULL saledate | 0 | Puuduv kuupäev |
| NULL totalprice | 0 | Puuduv summa |
| Tuleviku kuupäevad | 9 | Kuupäev > tänane |
| **KOKKU probleeme** | **5509** | Korduvad kirjed, puuduvad väärtused ja ebaloogilised kuupäevad. |

**Prioriteetide järjekord:**
1. **customer_id puudumine** - ei saa siduda klienti müügiga -> ei saa teha kliendianalüüsi -> **ÄRIMÕJU -> kõrge**
2. **duplikaadid** - topeltmüügid -> ebausaldusväärne kogukäive -> **ÄRIMÕJU -> keskmine kuni kõrge**
3. **tuleviku kuupäevad** - väike arv -> lihtne parandada -> ei mõjuta suurt pilti -> **ÄRIMÕJU -> madal**

**Peamine järeldus:**
* andmekvaliteedi probleemid, mis mõjutavad nii analüüsi täpsust kui ka andmete usaldusväärsust!
* enne andmete kasutamist aruandluses või otsuste tegemisel tuleb järgmiseks läbi viia andmete puhastamine ja valideerimine, et tagada korrektne ja usaldusväärne analüüsi baas.

---

#### 2. Kliendiandmed
Leitud **562** probleemset rida — Puuduvate emailidega kliendid on sisuliselt anonüümsed kliendid, kelle puhul pole selge, kui paljud neist on erinevad inimesed ning kellele ei saa muuhulgas ka e-posti teel teateid saata. Duplikaatsete e-mailidega kliendid moonutavad statistilisi andmeid oste sooritanud klientide arvu kohta ning näiteks ka seda, kui palju kliente erinevates linnades tegelikult on.

| **Kategooria** | **Leitud probleeme** | **Kirjeldus** |
| :--- | :--- | :--- |
| Duplikaatsed e-mailid | 128 | Sama e-mail mitmel kliendil |
| NULL eesnimi | 0 | Puuduv kliendi eesnimi |
| NULL perenimi | 0 | Puuduv kliendi perenimi |
| Ebajärjekindlad linnanimed | 54 | Erinevad nimekujud (nt tallinn vs Tallinn) |
| NULL telefon/e-mail | 380 | Puuduvad kontaktandmed |
| **KOKKU probleeme** | **562** | |

---

#### 3. Tooteandmed
Leitud **12** probleemset rida — Tooteanalüüsi mõjutab kõige rohkem tootenimede dublikaadid.

| **Kategooria** | **Leitud probleeme** | **Kirjeldus** |
| :--- | :--- | :--- |
| Duplikaatsed nimed | 12 | Sama tootenimi mitu korda |
| NULL nimi/hind | 0 | Puuduvad kriitilised väljad |
| Loogilised vead | 0 | Negatiivne või äärmuslik hind |
| Ebajärjekindlad kategooriad | 0 | Erinevad nimekujud (Shoes vs shoes) |
| NULL kategooria | 0 | Puuduv klassifitseerimine |
| **KOKKU probleeme** | **12** | |

---

#### 4. Kvaliteedikontroll
Leitud **1268** probleemset rida — Kõige kriitilisem on 664 hinnaerinevust, 592 klienti, kes pole kunagi ostnud.

| **Kategooria** | **Leitud probleeme** | **Kirjeldus** |
| :--- | :--- | :--- |
| Orbid kliendid | 0 | Müük viitab olematule kliendile |
| Orbid tooted | 0 | Müük viitab olematule tootele |
| Hinna ebakõlad | 664 | Müügihind ei klapi tootehinnaga |
| Vaimkliendid | 592 | Klient ei ole kunagi ostnud |
| Vaimtooted | 12 | Toodet pole kunagi müüdud |
| **KOKKU probleeme** | **1268** | |

---

### SUURIM ÜLLATUS:
* Kvaliteedikontrolli tulem - 664 hinnaerinevust.
* Müügiandmete dublikaadid mõjutavad oluliselt UrbanStyle kogukäivet.

### SOOVITUS TOOMASELE:
* Andmeid ei saa praegu usaldada!
* Kõige kriitilisemad on müügi- ja tooteandmete tabelid.
* Leida hindade ebakõla põhjus.
* Alustada tuleks dublikaatide puhastamisega.

### PUUDUVAD ANDMED:
* Hinnaebakõlad - kas tootehind või müügihind on õige?
* Customer_id
* telefon/email
