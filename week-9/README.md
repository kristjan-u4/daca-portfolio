# Nädal 9: Karjääri ettevalmistus

## AI kasutamine

### NotebookLM

* Et paremini aru saada, mida tähendavad DACA programmi ja käesoleva repositooriumi kontekstis mõisted **portfoolio** ja **projekt**, pöördusin küsimusega AI poole, andes allikana sisendiks käesoleva repositooriumi URL-i. Vastuseks sain, et kataloogid, kus asuvad iganädalased tööd (nt. praegune, **week-9**), on projektid, mis kõik kokku moodustavad portfoolio.
* Lisaks nädalapõhistele projektikataloogidele on mu repositooriumisse lisandunud hulk abikatalooge, näiteks viimasel nädalal, seoses **Aider**'i seadistamisega, `bin` ja `config`. Et projektikatalooge abikataloogidest eristada, näen vajadust luua `portfolio` kataloog, kuhu koondada projektikataloogid. AI kinnitas, et mu mõte on hea ja soovitas mul plaanitud tegevus ära teha.
* Oma grupitöö ülesande (peer review HR vaatepunktist) tegemiseks kogusin GitHubist kokku meeskonnakaaslase nädal 0-8 projektide README-failide sisu ning neis viidatud SQL päringud, Pythoni skriptid ja Jupyter notebook'id, et koondada need kokku ühtsesse markdown-faili. Andsin AI-le allikatena sisendiks meeskonnakaaslase GitHub repositooriumi URL-i ning nimetatud markdown-faili, mille alusel AI genereeris minu jaoks peer review dokumendi markdown-formaadis. Võib öelda, et AI tegi 95% tööst ära. Minu osaks oli allikate koostamine AI jaoks ja kvaliteedikontroll AI töö tulemustele.

### Google Gemini chatbot

* Kui ma esialgu testisin NotebookLM kasutamist peer review tegemiseks enda repositooriumi peal, siis andsin ma NotebookLM-ile allikatena sisendiks ette minu hinnangul vajaminevate failide GitHub URL-id igaühe eraldi, mille peale NotebookLM vastas tõrketeatega: "Teie märkmiku üleslaaditavate failide piirarv on täis". Pöördusin Gemini poole, kes soovitas mul koondada kõik info ühte markdown-faili, kasutades üksikute failide "lehekülgedeks" jaotamiseks XML-tääge. Toimisin vastavalt soovitusele, mille tulemusena NotebookLM tõrge kadus.
