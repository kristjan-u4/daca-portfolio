# Nädal 9: Karjääri ettevalmistus

## AI kasutamine

### NotebookLM

* Et paremini aru saada, mida tähendavad DACA programmi ja käesoleva repositooriumi kontekstis mõisted **portfoolio** ja **projekt**, pöördusin küsimusega AI poole, andes allikana sisendiks käesoleva repositooriumi URL-i. Vastuseks sain, et kataloogid, kus asuvad iganädalased tööd (nt. praegune, **week-9**), on projektid, mis kõik kokku moodustavad portfoolio.
* Lisaks nädalapõhistele projektikataloogidele on mu repositooriumisse lisandunud hulk abikatalooge, näiteks viimasel nädalal, seoses **Aider**'i seadistamisega, `bin` ja `config`. Et projektikatalooge abikataloogidest eristada, näen vajadust luua `portfolio` kataloog, kuhu koondada projektikataloogid. AI kinnitas, et mu mõte on hea ja soovitas mul plaanitud tegevus ära teha.
* Oma grupitöö ülesande (peer review HR vaatepunktist) tegemiseks kogusin GitHubist kokku meeskonnakaaslase nädal 0-8 projektide README-failide sisu ning neis viidatud SQL päringud, Pythoni skriptid ja Jupyter notebook'id, et koondada need kokku ühtsesse markdown-faili. Andsin AI-le allikatena sisendiks meeskonnakaaslase GitHub repositooriumi URL-i ning nimetatud markdown-faili, mille alusel AI genereeris minu jaoks peer review dokumendi markdown-formaadis. Võib öelda, et AI tegi 95% tööst ära. Minu osaks oli allikate koostamine AI jaoks ja kvaliteedikontroll AI töö tulemustele.

### Google Gemini chatbot

* Kui ma esialgu testisin NotebookLM kasutamist peer review tegemiseks enda repositooriumi peal, siis andsin ma NotebookLM-ile allikatena sisendiks ette minu hinnangul vajaminevate failide GitHub URL-id igaühe eraldi, mille peale NotebookLM vastas tõrketeatega: "_Teie märkmiku üleslaaditavate failide piirarv on täis_". Pöördusin Gemini poole, kes soovitas mul koondada kõik info ühte markdown-faili, kasutades üksikute failide "lehekülgedeks" jaotamiseks XML-tääge. Toimisin vastavalt soovitusele, mille tulemusena NotebookLM tõrge kadus.

### Aider + Gemini 2.5 Flash

* Jätkasin eelmisel nädalal avastatud AI paarisprogrammeerimise töövahendiga **Aider** tutvumist. Kasutasin Aider'it käesoleva repositooriumi korrastamiseks. Aideri abiga teisaldasin nädalapõhised projektid `portfolio` kataloogi ja lisasin projektide nimedes nädala järjekorranumbri ette numbri 0, et week-10 tulekuga säiliks loomulik ajalises järjekorras sorteerimine. Lisaks parandasin Aider + AI mudeli abiga Pythoni koodis ja Shell skriptides vigu, mis tekkisid seoses failide teisaldamisega.
* Lisasin Aider + AI mudeli jaoks instruktsioonid, mis kehtivad üle terve repositooriumi: [config/development/ai_global_instructions.md](../../config/development/ai_global_instructions.md)
* Lisasin Aider'i mugavaks käivitamiseks vajaliku kontekstiga (AI mudel, vaikimisi sisseloetavad failid, instruktsioonid AI mudeli kaoks) Shell skripti: [bin/aider.sh](../../bin/aider.sh)
