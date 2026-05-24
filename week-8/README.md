# Nädal 8: Python APIs

## Minu roll

### Roll D: Automation Script

Minu ülesandeks oli kirjutada Pythoni skript `pipeline.py`, mis seob teiste meeskonnaliikmete poolt arendatud moodulid kokku ühtseks **ETL Pipeline**'iks.

* `pipeline.py` võtab argumentidena sisendiks kuupäevavahemiku, mis edastatakse **Roll A** poolt arendatud moodulile `data_fetcher.py`, mis esindab **E** ehk **Extract** etappi ETL Pipeline'is. Nimetatud moodul kasutab etteantud ajavahemikku filtrina müügiandmete pärimisel Supabase'ist.
* Lisaks müügiandmetele kasutab `pipeline.py` moodulit `data_fetcher.py` ka kliendiandmete pärimiseks Supabase'ist.
* Supabase'ist päritud müügiandmed puhastatakse, kasutades selleks **Roll B** poolt arendatud moodulit `transform.py`, mis esindab **T** ehk **Transform** etappi ETL Pipeline'is.
* Puhastatud müügiandmeted antakse uuesti sisendiks moodulile `transform.py`, et agregeerida müügiandmed nädala-põhiselt ja arvutada välja KPI mõõdikud.
* Moodulit `transform.py` kasutatakse puhastatud müügiandmete ühendamiseks kliendiandmetega.
* Nädala-põhiselt agregeeritud müügiandmed antakse sisendiks **Roll C** poolt arendatud moodulile `visualize_export.py`, mis esindab **L** ehk **Load** etappi ETL Pipeline'is. Etteantud sisendi alusel koostab nimetatud moodul joondiagrammi, mis näitab summaarset müügitulu nädala lõikes.
* Mooduli `transform.py` abil välja arvutatud KPI mõõdikud visualiseeritakse moodulit `visualize_export.py` kasutades.
* Koostatud joondiagramm ja KPI mõõdikute visualiseering antakse uuesti sisendiks moodulile `visualize_export.py`, mille alusel salvestatakse nimetatud sisendid HTML failidena. Lisaks antakse sisendina ette mooduli `transform.py` poolt ühendatud müügi- ja kliendiandmed, et salvestada need CSV failina.
* Salvestatud failide nimekirja annab `pipeline.py` uuesti sisendiks moodulile `visualize_export.py`, et viimane saaks teostada täiendavat logimist ja vajaduse korral välja saata teavitused.
* `pipeline.py` logib kõigi kolme etapi alguse ja lõpu ja lisab täiendavat logimist seal, kus eraldiseisvad moodulid seda juba ei tee.
* `pipeline.py` mõõdab terve ETL Pipeline'i läbimiseks kulunud aega sekundites ja logib tulemuse.
* Juhul, kui mõne etapi läbimise juures tekib viga, siis `pipeline.py` püüab selle kinni ja logib koos detailidega vea tekkepõhjuse kohta.

### Automatiseerimine

ETL Pipeline automatiseerimise edasiste võimaluste uurimiseks kirjutasin sh skripti `bin/weekly_demo.sh`, mis demonstreerib, kuidas `pipeline.py` skriptile ajavahemikuna ette anda käesolevale nädalale eelnev nädal. Esitlusel näitasin veel, kuidas nimetatud sh skripti saab seadistada programmiga `crontab`, et panna see automaatselt jooksma kord nädalas etteantud ajal.

## AI kasutamine

### Google Gemini

* Vastas küsimustele, kuidas üht või teist eesmärki Pythonis saavutada (näiteks kuidas lugeda terminalilt sisendiks ette antud kuupäevavahemikku).
* Aitas pipeline'i arendamisel tekkinud tehniliste tõrgete lahendamisel.
* Vastas erinevatele `bin/weekly_demo.sh` skripti kirjutamisel tekkinud küsimustele, nt. kuidas praeguse kuupäeva alusel eelmist nädalat ajavahemikuna välja arvutada.
* Informeeris mind, et on olemas terminalil põhineb AI paarisprogrammeerimise tööriist nimega **Aider**, mis aitab arendusprotsessis AI kasutamist automatiseerida ja vastas mu küsimustele, kuidas seda seadistada ja kasutada.

### Aider + Gemini 2.5 Flash

**Aider** on terminalil põhinev AI paarisprogrammeerimise tööriist, millega puutusin sel nädalal esimest korda kokku. Aideri kasutamiseks tuli valida AI mudel ja ette anda tolle API key. Mina kasutasin mudelina **Gemini 2.5 Flash**, mida saab teatud limiidini (20 korraldust päevas) kasutada tasuta.

Minu eesmärgiks oli ka teiste rollide ülesanded iseseisvalt läbi teha pärast meeskonnatöö esitlust, et mõista ETL etappide sisu sügavamalt ja selleks, et Pythoni teekide Pandas ja Plotly kasutamist harjutada. Ma soovisin tööprotsessi kiirendada, kuid ma olin jõudnud arusaamiseni, et Google Gemini chatbot ei ole selleks piisav.

* Aideri abil andsin AI-le sisendiks eraldiseisvad .py failid ja juhendid funktsioonide kirjutamiseks, mida `pipeline.py` vajab.
* Juhendites ma kirjeldasin, mida iga funktsioon sisendiks võtab, mis on sisendi struktuur, mida funktsioon tegema peab ja mille tagastama.
* AI viis failides muudatused sisse vastavalt etteantud juhendile.
* Kui AI oli failides muudatused teinud, siis ma kontrollisin väljundit ja kui see sobis, tegin `git commit` ja `git push`. Aideri seadistamisel ma keelasin automaatsed commit'id ära, et väljundit ise kontrollida.
* Kui väljund ei olnud vastuvõetav, siis lasin AI-l teha muudatused uuesti. Detailsemad probleemid lahendasin ise, kasutades ka Google Gemini chatboti abi.

### NotebookLM

* Küsimusele, kus ajakulu logimine tuleb teostada, sain vastuseks, et see tuleb teha main-blokis, mitte run_pipeline() funktsioonis.
* Skripti argumentide lugemise tuli AI väitel samuti teostada main-blokis ja anda loetud argumendid edasi argumentidena run_pipeline() funktsioonile.

## Tehniline teostus

* **Andmeallikas:** PostgreSQL (Supabase).
* **Pythoni moodulid:** logging, time, argparse, datetime.
* **ETL Pipeline moodulid:** data_fetcher, transform, visualize_export.
* **Töövahendid:** VS Code, Git, Aider, Ubuntu terminal.

## Pipeline käivitamine (Ubuntu terminal)

1. Veendu, et on Python installitud
2. Mine käesoleva portfoolio juurkataloogi ja loo Pythoni virtuaalkeskkond: `python3 -m venv .venv`
3. Aktiveeri Pythoni virtuaalkeskkond: `source .venv/bin/activate`
4. Vajaminevad teegid on loetletud **requirements.txt** failis. Installi need: `pip install -r requirements.txt`
5. Seadista andmebaasiühendus, kasutades `.env` faili.
6. Käivita pipeline sobiva kuupäevavahemikuga:

```bash
python3 week_8/pipeline.py --start-date=2024-01-01 --end-date=2025-02-28
```

## Lingid
