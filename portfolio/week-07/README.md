# Nädal 7: Python Pandas — RFM kliendisegmenteerimine

## Minu roll

### Roll C: Analysis — RFM kliendisegmenteerimine

* Uurisin Roll B poolt puhastatud müügiandmeid kuni **viitekuupäevani 28.02.2025**
* Kasutades Pandase `qcut()` meetodit, arvutasin iga kliendi kohta välja 3 mõõdikut, mille väärtuseks on **hinne skaalal 1-5**:
  * **Recency (R)** iseloomustab kõige viimasest ostust möödunud aega.
    * Aluseks olev mõõdik: viitekuupäeva ja viimase ostukuupäeva vahe.
    * Mida lühem aeg, seda kõrgem hinne.
  * **Frequency (F)** iseloomustab ostude sagedust.
    * Aluseks olev mõõdik: tellimuste arv kliendi kohta.
    * Mida suurem ostude arv, seda kõrgem hinne.
  * **Monetary (M)** iseloomustab ostude rahalist väärtust.
    * Aluseks olev mõõdik: ostude kogusumma eurodes kliendi kohta.
    * Mida suurem kogusumma, seda kõrgem hinne.
* Summeerisin R, F ja M mõõdikud ja leidsin seeläbi iga kliendi jaoks **RFM skoori**, mille alusel jaotasin kliendid segmentidesse:
  * **VIP Champions:** skoor 13-15,  kokku **453** klienti
  * **Loyal:** skoor 10-12,  kokku **677** klienti
  * **Potential:** skoor 7-9,  kokku **768** klienti
  * **At Risk:** skoor 4-6,  kokku **525** klienti
  * **Lost:** skoor 3,  kokku **117** klienti
* Andmed klientide RFM skooride ja segmentidega edastasin sisendina Roll D-le andmete visualiseerimiseks.

## Peamised leiud

* Kõige arvukam on potentsiaalsete klientide segment - 768 klienti. See on UrbanStyle’i jaoks kõige olulisem kasvumootor ja "toormaterjal".
* Lojaalseid kliente on rohkem (677 klienti), kui riskantseid (525 klienti). See näitab, et UrbanStyle’i kliendibaas on hetkel tervislik ja brändi fookus on õige.
* Riskantseid kliente on rohkem, kui VIP kliente (453 klienti). See on ohumärk, mis viitab sellele, et me kaotame väärtuslikke kliente kiiremini, kui suudame neid tippu (VIP-iks) kasvatada.

## AI kasutamine

### Google Gemini

* Õppejuhendis oli näidatud, kuidas R, F ja M lähteandmed grupeeritakse kliendi lõikes eraldi ja lõpuks ühendatakse (merge), aga mul tekkis hüpotees, et seda kõike saaks teha ühe meetodiga (agg).
  Küsisin AI-lt, kas minu metoodika annab sama tulemuse, mis õppematerjalis toodu. AI vastas, et annab ning minu meetod olevat ka loetavam ja jõudluse mõttes kiirem.
* Õpetas, kuidas qcut() parameetri q=5 korral hinnete list F ja M mõõdikute jaoks genereerida dünaamiliselt ja genereeritud listi pealt genereerida ümberpööratud list R-mõõdiku jaoks.
* Mul tekkis F-skoori arvutamisel tõrge: `ValueError: Bin edges must be unique: Index([1.0, 2.0, 2.0, 3.0, 5.0, 77.0], dtype='float64', name='total_purchases')`. Küsisin AI-lt, millest see tuleb ja kuidas probleemi lahendada.
  AI vastas, et see viga tekib siis, kui andmetes on **liiga palju korduvaid väärtusi** ja soovitas mul kasutada `.rank(method='first')`. AI soovitatud kooditäiendus eemaldas tõrke.

### NotebookLM

* Abistas äritõlgenduste sõnastamisel peamiste etteantud kliendisegmentide võrdlemisel minu poolt tehtud tähelepanekute pinnalt.

## Tehniline teostus

* **Andmeallikas:** PostgreSQL (Supabase).
* **Tööriistad:** Python, Pandas, SQLAlchemy, Supabase, Plotly Express, Jupyter Lab.
* **Meetodid:** `groupby`, `agg`, `qcut`, `rank`.

## Kuidas .ipynb notebook'i käivitada (Ubuntu Linux näitel)

1. Veendu, et Python on installitud
2. Mine käesoleva repositooriumi juurkataloogi ja loo Pythoni virtuaalkeskkond: `python -m venv .venv` (kui `python` ei tööta, proovi `python3`)
3. Aktiveeri Pythoni virtuaalkeskkond: `source .venv/bin/activate`
4. Vajaminevad teegid on loetletud **requirements.txt** failis. Installi need: `pip install -r requirements.txt`
5. Seadista andmebaasiühendus, kasutades `.env` faili. Vajaduse korral pöördu käesolevasse punkti tagasi, kui punktis 7. esineb Supabase'i ühendusega seotud veateade.
6. Käivita **Jupyter Lab** terminalis: `jupyter lab`. Jupyter Lab on Jupyter Notebook kaasaegsem edasiarendus.
7. Vali Jupyter Lab keskkonnas projekti week-07 alamkataloogidest soovitud .ipynb fail ja klõpsa hiirega **Restart the kernel and run all cells** valikul.

## Lingid

* **Meeskondlik .ipynb notebook:** [week7_rfm_complete.ipynb](./team/week7_rfm_complete.ipynb)
* **Individuaalne .ipynb notebook**, mille koostamisel simuleerisin ka teisi rolle, mis võimaldas mul teiste meeskonnaliikmetega samaaegselt töötada enda alamülesandega: [individual/week7_rfm_role_c.ipynb](./individual/week7_rfm_role_c.ipynb)
