# Nädal 5: Visualiseerimise disain

## Projekti ülevaade
Sel nädalal oli fookuses andmete visualiseerimine ja dashboardi disain UrbanStyle.ltd sidusrühmadele. Mina täitsin grupitöös **Roll A (Tegevjuht Kristi Tamme vaade)** ülesandeid. Minu eesmärk oli luua kõrgtaseme ülevaade ettevõtte käekäigust, vastates Kristi peamisele küsimusele: "Kas me kasvame?". Kuna andmete visualiseerimistööriistade valikul olen otsustanud minna **Track B** teed, siis kasutasin dashboardi loomisel programmeerimiskeelt **Python** ning selle teeke **Plotly** ja **Streamlit**.

## Dashboardi eelvaade
![CEO Dashboardi ekraanipilt](week-5/individual/week_5_ceo_dashboard_screenshot.png)
*Märkus: Ülaltoodud pilt on vaade valmis Streamliti rakendusest, mis on suunatud tegevjuhile.*

## AI kasutamine

### Google Gemini

* Plotly ja Streamlit seadistamisjuhendis olev näidisrakendus laeb kõik 10 118 rida `sales` tabelist mällu, kasutades selleks Pythoni **Supabase** teeki, mis suhtleb Supabase andmebaasiga üle HTTP-põhise API. Kuna antud lahendus ei ole skaleeruv (mis siis, kui `sales` tabelis oleks 10 miljonit rida?), siis otsustasin kirjutada lähtekoodi ümber nii, et andmete agregeerimine ja filtreerimine toimuks andmebaasis, kasutades SQL päringuid. Uurisin AI-lt, kuidas Pythoni Supabase teeki saaks kasutada SQL päringute tegemiseks. AI vastas, et puhta SQL kasutamiseks on tarvis teisi teeke. AI soovitas mul installida **SQLAlchemy** teek, abistas mind sellega ja õpetas mind, kuidas seda kasutada.
* Koostöös AI-ga selgitasime välja, et Pythoni moodul `dateutil.relativedelta` sobib suurepäraselt suvalise etteantud ajavahemiku põhjal sellele eelneva võrdlusperioodi arvutamiseks. See osutus vajalikuks KPI koostamisel, mis näitab 2024. aasta käibe muutust võrdluses 2023. aastaga.
* AI abiga leidsime lahendused erinevatele Plotly graafikute välimuse kohandamisega seotud küsimustele (nt. kuidas muuta trendijoone värv UrbanStyle'i brändivärviks).

AI on asendamatu abiline, kellega koos Pythonit õppida.

### NotebookLM

* Andis infot selle nädala grupitöö portfoolio integratsiooni nõuete kohta.
* Aitas mind käesoleva README faili jaoks näidispõhja tegemisel.

## Ärilised järeldused (Insights) Kristi Tammele
Analüüsides UrbanStyle'i koondandmeid, tuvastasin järgmised olulised punktid juhatuse koosolekuks:

1. **Kasvutrend 2023-2024:** Meie igakuine müügitulu 2024. aastal kasvas 2023. aastaga võrreldes 19%, kusjuures 2024. aasta viimase kvartali kasv on olnud eriti märkimisväärne. See kinnitab, et UrbanStyle'i strateegia aastatel 2023-2024 on olnud õigel teel.
2. **Puudulikud andmed alates 2025:** Alates 2025. aastast on andmetes lüngad ja esineb teisi anomaaliaid, mistõttu ei ole alates 2025. aastast võimalik müügitrende objektiivselt hinnata.

## Tehniline teostus
* **Andmeallikas:** PostgreSQL (Supabase) `sales` tabel.
* **Tööriistad:** Python, SQLAlchemy, Pandas, Plotly Express, Streamlit.
* **Disainipõhimõtted:** Järgisin **Tufte** põhimõtteid (kõrge data-ink ratio) ja **Knaflici** disainerimõtlemist. Asetasin kõige olulisemad KPI kaardid ekraani ülaossa (F-muster), et Kristi saaks olukorrast aru 10 sekundiga. Kasutasin UrbanStyle brändivärvi (#009B8D teal) trendide rõhutamiseks.

## Meeskonna koondraport
Meie meeskonna ühine investorite koondvaade, mis sünteesib CEO, turunduse ja operatsioonide vaated, asub [siin](https://docs.google.com/presentation/d/1xLmbXssHMxNhEsh4dl6HjVJakhiVlHHW/edit?slide=id.p1#slide=id.p1).

## Kuidas rakendust käivitada (Ubuntu Linux näitel)
1. Veendu, et sul on Python installitud
2. Mine käesoleva projekti juurkataloogi ja loo Pythoni virtuaalkeskkond: `python -m venv .venv` (kui `python` ei tööta, proovi `python3`)
3. Aktiveeri Pythoni virtuaalkeskkond: `source .venv/bin/activate`
4. Vajaminevad teegid on loetletud **requirements.txt** failis. Installi need: `pip install -r requirements.txt`
5. Käivita rakendus terminalist: `streamlit run week-5/individual/dashboard/app.py`

## Lähtekood

* Streamlit rakendus: [app.py](week-5/individual/dashboard/app.py)
* Abiskriptid, millest app.py sõltub, asuvad samas kataloogis.
* SQL päringute mallid, mida Pythoni kood kasutab, asuvad sql alamkataloogis. **NB!** Päringutes tuleb dünaamilised parameetrid asendada, kui on vajalik neid Supabase'is käsitsi jooksutada.
