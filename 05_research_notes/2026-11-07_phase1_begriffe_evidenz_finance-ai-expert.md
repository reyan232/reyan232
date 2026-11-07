# Bericht finance-ai-expert: Phase 1 (Themenfokussierung), 2026-11-07

> Herkunft: KI-generiert (finance-ai-expert, 2026-11-07) – nicht zur Abgabe. Arbeitsgrundlage für den Orchestrator. Ich habe keine Dateien geschrieben.

> **Hinweis des Orchestrators (2026-11-07):** Die Metadaten der hier genannten Kandidaten wurden nachträglich per Crossref geprüft (Ergebnis in `03_sources/literature.csv`, Spalten `metadata_status`/`metadata_evidence`; Abweichungen in `notes`). Die Statusangaben in diesem Bericht („NICHT_VERIFIZIERT“) sind damit für die Metadaten überholt; Peer Review und Inhalte bleiben ungeprüft.


## 0. Wichtigste Punkte vorab

1. **Keine Quelle konnte verifiziert werden.** Alle vier erlaubten Verifikationshosts haben in dieser Sitzung nicht aufgelöst (`getaddrinfo ENOTFOUND`): api.crossref.org, doi.org, www.econbiz.de und api.openalex.org. Laut Hinweis des Tools habe ich danach keine weiteren Hosts mehr versucht.
   - **Freigabe nötig:** Diese Hosts müssen in den Netzwerkeinstellungen der Sitzung freigegeben werden, damit die Kandidaten verifiziert werden können.
   - **Folge für die Statusangaben:** Alle Angaben unten stammen nur aus WebSearch-Ergebnissen. Die Treffer-URLs habe ich nicht selbst geöffnet.
   - Für alle Kandidaten gilt deshalb: `metadata_status = NICHT_VERIFIZIERT`, `access_level = NUR_METADATA` und `peer_review_status = UNKLAR`.
   - Inhaltliche Hinweise stammen aus Zusammenfassungen von Abstracts oder Katalogeinträgen durch die Suchmaschine. Ich habe sie nicht selbst am Abstract geprüft. Daher gibt es keine Seitenangaben und keine Detailbefunde.
2. **Die Evidenzlage bestätigt die Hypothese in `topic_options.md`: Sie ist sehr dünn.**
   - Ich habe keine begutachtete empirische Studie (Fallstudie, Umfrage, Interviewstudie) gefunden, die KI-Agenten in der CFO-Funktion realwirtschaftlicher Unternehmen untersucht.
   - Was es an agentenspezifischer Literatur gibt, ist begrifflich und konzeptionell (Wirtschaftsinformatik, BPM) oder prototypisch. Die Prototypen stammen meist aus der Abschlussprüfung.
   - Zur Verbreitung gibt es bislang nur Anbieter- und Beratungsumfragen. Sie sind ausgeschlossen, ihre Zahlen habe ich bewusst nicht übernommen.
   - Hinweis, keine Quelle: Das Journal of Emerging Technologies in Accounting (JETA) hat einen Call for Papers für eine Special Section „Agentic AI in auditing and accounting“ veröffentlicht (Einreichungsfrist 31.05.2026). Begutachtete Accounting-Literatur zu Agenten entsteht also gerade erst.
3. **Die ältere Agentenliteratur ist für die Abgrenzung relevant.**
   - Gemeint sind die klassische Agententheorie und Multi-Agenten-Systeme für Continuous Auditing aus den Jahren um 2000–2007.
   - Sie zeigt, dass „Agent“ im Rechnungswesen kein neues Konzept ist. Neu sind LLMs als Steuerkern, Planung in natürlicher Sprache und flexible Werkzeugnutzung.

---

## 1. Begriffliche Entscheidungspunkte (vom Studenten zu entscheiden)

| # | Entscheidungspunkt | Optionen | Quellenbasis (Status s. Abschnitt 6) |
|---|---|---|---|
| D1 | Definitionsansatz | (a) Etikett („KI-Agent“ = was so genannt wird) oder (b) **Merkmalskatalog** (Zielorientierung, Planung, Werkzeugnutzung, Gedächtnis, Autonomiegrad). Option (b) trägt die Abgrenzung belastbarer, weil der Begriff in Praxis und Teilen der Literatur unscharf verwendet wird. | Q050, Q053, Q054; Hinweis Sapkota u. a. (Problem: „AI agents“ und „agentic AI“ werden vermischt) |
| D2 | Agentur binär oder graduell | Graduell bedeutet: Autonomie als Kontinuum je Funktionstyp (Informationsaufnahme, Analyse, Entscheidungsauswahl, Ausführung). Das passt zu Freigabestufen im Finanzbereich. | Q051; Q052 (Delegation); Hinweis Chan u. a. 2023 (vier Dimensionen zunehmender Agentur) |
| D3 | Einzelagent vs. agentische KI / Multi-Agenten-System | Abgrenzung (1) einzelner, werkzeugnutzender LLM-Agent, (2) mehrere spezialisierte Agenten mit Orchestrierung („agentic AI“), (3) klassische Multi-Agenten-Systeme ohne LLM. Zu klären ist, ob (2) im Scope liegt. | Q054 (grenzt agentische KI von klassischen autonomen Agenten und Multi-Agenten-Systemen ab), Q055 (Fünf-Schichten-Architektur), Q058 (historisches Multi-Agenten-System) |
| D4 | Abgrenzung zu RPA/IPA | RPA: regelbasiert, strukturierte Daten, das Informationssystem bleibt unverändert. IPA: RPA plus KI/ML-Bausteine. **Offen ist die Grenzziehung:** Ist eine IPA-Strecke mit LLM-Baustein schon ein Agent? Vorschlag: nur bei eigener Planung und eigener Werkzeugauswahl. | Q056; Hinweis van der Aalst/Bichler/Heinzl 2018 |
| D5 | Abgrenzung zu GenAI, Chatbot und Copilot | GenAI ist eine Technologieklasse (Inhaltserzeugung). Ein Chatbot ist eine reaktive Dialogschnittstelle. Ein Copilot ist ein LLM in der Fachanwendung, bei dem der Mensch entscheidet. Ein Agent ergänzt das LLM um Planung, Werkzeuge, Gedächtnis und Handeln. Zu entscheiden ist, ob „Copilot“ als Vorstufe mitbehandelt wird. | Q053; Hinweise Feuerriegel u. a. 2024, Gu u. a. 2024 („co-piloted auditing“) |
| D6 | Konzept für Human-in-the-loop und Governance | „Framed autonomy“ (Autonomie innerhalb definierter Ziele und Rahmenbedingungen) als Ordnungsbegriff oder Delegationsrahmen nach Baird/Maruping | Q057, Q052 |
| D7 | Begriff „Finanzfunktion“ | Teilbereiche festlegen. Abschlussprüfung (externe Prüfer), Banken und Handel/Trading ausschließen. Viele Quellen zu „agentic AI in finance“ betreffen Finanzmärkte, sind also Nicht-Zielbereich. Das gilt auch für das Beispiel auf Folie 48. | Folie 14 (Aufgabenkontext, kein Beleg) |
| D8 | Deutsche Terminologie | „KI-Agent“, „agentische KI“, „Multi-Agenten-System“; Anglizismen zurückhaltend und definiert verwenden (V S. 17–18) | Formvorgabe |

Abgleich mit Folien 46–48: Die gefundene Literatur stützt die Kernidee der Folien, dass Agenten eigenständig planen und handeln (Planungs- und Aktionsmodul in Q053, Autonomie in Q050). Sie ergänzt aber zwei Nuancen: Agentur ist graduell (Q051, Q052), und agentische KI ist eine eigene Systemebene über dem Einzelagenten (Q054, Q055). Die Folien bleiben Definitionseinführung und sind kein Beleg.

---

## 2. Evidenzbasierte Abgrenzung: Merkmal × Technologie

Legende:
- **[I]** = eigene Einordnung oder Allgemeinwissen, noch nicht am Text belegt.
- **[H]** = Hinweisquelle, nicht in der CSV, NICHT_VERIFIZIERT.
- Für alle Q-IDs gilt: Metadaten NICHT_VERIFIZIERT, Zugriff NUR_METADATA, Inhalt aus Suchzusammenfassungen.

| Merkmal | RPA | IPA | Analytics/ML | GenAI-Chatbot | Werkzeugnutzender LLM-Agent | Agentische KI / LLM-Multi-Agenten-System | Belege |
|---|---|---|---|---|---|---|---|
| Steuerungslogik | Wenn-dann-Regeln, strukturierte Daten | Regeln plus KI-Bausteine | statistisches Lernen, Ausgabe ist Prognose oder Score | Generierung auf Prompt | LLM als Steuerkern | mehrere Agenten plus Orchestrierung | Q056, Q053, Q055; [H] van der Aalst 2018, Feuerriegel 2024 |
| Zielorientierung | nein, Ablauf vorgegeben | nein [I] | nein, kein Handlungsziel [I] | reaktiv [I] | ja, Aufgabenziel | ja, Ziel wird auf Agenten verteilt | Q050 (Proaktivität, nur sekundär gesehen), Q053; [H] Chan 2023 |
| Mehrstufige Planung | nein | eingeschränkt [I] | nein | nein | ja (Planungsmodul) | ja, dynamische Aufgabenzerlegung | Q053; [H] Sapkota 2025 |
| Werkzeugnutzung / Handeln in Systemen | ja, fest skriptiert (Oberfläche) | ja, skriptiert | nein [I] | nein | ja (Aktionsmodul, Werkzeuge/APIs) | ja, über mehrere Systeme | Q053, Q055 (Schicht „data-centric perception and action“), Q056 |
| Gedächtnis | nein [I] | nein [I] | nur Modellparameter [I] | Dialogkontext | Kurz- und Langzeitgedächtnis (Gedächtnismodul) | persistentes Gedächtnis | Q053; [H] Sapkota 2025 |
| Unstrukturierte Eingaben | gering [I] | mittel (z. B. Dokumentenerkennung) [I] | modellabhängig | hoch | hoch | hoch | Q056 (Richtung RPA zu IPA), sonst [I] |
| Autonomiegrad | hoch automatisiert, aber nicht autonom [I] | wie RPA [I] | entscheidungsunterstützend | Mensch löst jede Interaktion aus | gestuft wählbar | höher, Governance-Rahmen nötig | Q051, Q052, Q057 |
| Human-in-the-loop | Ausnahmebehandlung [I] | Ausnahmebehandlung [I] | Mensch entscheidet | Mensch entscheidet | Freigabepunkte gestaltbar | „framed autonomy“, Erklärbarkeit, Dialogsteuerung | Q051, Q052, Q057 |
| Klassische Vorläufer | – | – | – | – | Softwareagenten (Autonomie, Reaktivität, Proaktivität, soziale Fähigkeit) | Multi-Agenten-Systeme 1990er/2000er, z. B. Continuous Auditing | Q050, Q058 |

**Querschnittsmerkmal Autonomie und Freigabe.** Analyseidee [I], noch nicht am Text geprüft:
- Das Raster aus Q051 (vier Funktionstypen × Stufen) ließe sich auf Finanzprozesse übertragen. Beispiel: Ein Agent darf Informationen beschaffen und analysieren, Buchungs- oder Zahlungsvorschläge aber nur zur Freigabe vorlegen.
- Q051 nennt laut Abstract-Zusammenfassung Zuverlässigkeit und Kosten von Entscheidungs- und Handlungsfolgen als Gestaltungskriterien. Das ist für Zahlungen und Buchungen anschlussfähig, wäre aber eine **Übertragung**.

---

## 3. Evidenzlage je Teilbereich (Frage 2)

### 3a. Einsatzfelder

| Teilbereich | Einsatzfeld (Stichwort) | Evidenztyp | Quelle | Bemerkung |
|---|---|---|---|---|
| Controlling | Grenzen von KI im Controlling (Komplexität, Kybernetik) | konzeptionell (semi-systematisches Review, empirisch validierte Forschungsfragen) | Q059 | nicht agentenspezifisch; **Gegenposition** zu hoher Autonomie |
| Controlling / Accounting | Vertikale GuV-Analyse: manuell vs. spezialisiertes GPT vs. Agent (GPT plus No-Code-Automatisierung) | Experiment/Prototyp (laut Suchzusammenfassung 150 experimentelle Fälle, größter Effizienzgewinn beim Agenten) | Q062 | Einzelautor, MDPI, Einzelaufgabe; Agentenbegriff und Design am Volltext prüfen (Open Access) |
| Controlling (Planung, Forecast, Berichtswesen) | – | keine begutachtete agentenspezifische Studie gefunden | – | Stufe-2-Suche per WebSearch erfolglos, Datenbanksuche nötig |
| Accounting / Prüfung | LLM-Audit-Agent: Wissensabruf (RAG) auf private Wissensbasen, Workflows mit Anfrageklassifikation und Multi-Agenten-Koordination, Prompts mit Prüfungsmethodik | prototypisch; Evaluation laut Abstract-Zusammenfassung erst geplant | Q061 | Kontext Abschlussprüfung, für die CFO-Funktion als **Übertragung** kennzeichnen |
| Accounting / Prüfung (historisch) | agentenbasiertes Continuous-Audit-Modell (ABCAM, mobile Agenten, fünf Szenarien) | konzeptionell/prototypisch | Q058 | Vorläufer ohne LLM, geeignet für die Begriffsgeschichte |
| Accounting / Prüfung | „Co-piloted auditing“: Prüfer plus Foundation Model | konzeptionell plus Demonstration | [H] Gu u. a. 2024 | Copilot-Stufe, kein autonomer Agent |
| Accounting (Berufsbild) | Rollen, Aufgaben und Fähigkeiten im KI-gestützten Rechnungswesen | Delphi-Studie plus Workshops | [H] Leitner-Hanetseder u. a. 2021 | KI allgemein, nicht Agenten; überschneidet sich mit Nr. 11 |
| Treasury | „Finance and Treasury 4.0“, RPA, ML; Treasury-Prozesse weitgehend virtuell | konzeptionell | Q060 | nicht agentenspezifisch; keine weitere begutachtete Treasury-Quelle gefunden |
| Übergreifend (Prozesse/IS) | agentisches Prozessmanagement: framed autonomy, Erklärbarkeit, Dialogsteuerung, Selbstmodifikation | konzeptionell (Manifest, Dagstuhl-Seminar) | Q057 | kein Finanzbezug, aber Rahmen für Governance |
| Übergreifend | Multi-Agenten-KI als Fünf-Schichten-Architektur | konzeptionell | Q055 | Analyseraster für die „betriebliche Basis“ [I] |
| Übergreifend | agentische KI im Unternehmen, Forschungsagenda (Design, Governance, Mensch-KI-Zusammenarbeit, Plattformen), Unternehmensbeispiel mit mehreren Agenten | konzeptionell (Catchword) | Q054 | Inhalt des Beispiels unbekannt |

### 3b. Erfolgsfaktoren und Voraussetzungen

Hier gibt es keine agentenspezifische empirische Evidenz für die CFO-Funktion. Die Zuordnung unten ist konzeptionell oder eine Übertragung.

| Faktor | Beleglage | Quellen |
|---|---|---|
| Daten und Wissensbasis | konzeptionell (Schicht „datenzentrierte Wahrnehmung und Aktion“); prototypisch (Wissensabruf auf private Wissensbasen) | Q055, Q061 |
| Prozessintegration | konzeptionell (agentenintegrierter Workflow; Autonomie im Prozessrahmen) | Q055, Q057 |
| Governance, Kontrollen, Freigaben | konzeptionell (framed autonomy, Erklärbarkeit; Delegationsmechanismen; Automatisierungsstufen; Governance als Forschungsagenda) | Q057, Q052, Q051, Q054 |
| Kompetenzen und Rollen | Übertragung aus KI- bzw. RPA-Studien | [H] Leitner-Hanetseder 2021; [H] Kokina u. a. 2021 (RPA-Rollen; als Übertragung kennzeichnen) |
| Auditierbarkeit / Prüfpfad | keine begutachtete Quelle gefunden; nur JETA-Call, Anbieter- und Verbandsmaterial | Rechercheauftrag |

### 3c. Risiken (Quellenlage)

- **Zuverlässigkeit und Halluzination:**
  - [H] Wood u. a. 2023, GenAI-Chatbot mit Accounting-Prüfungsfragen: schwächer bei Financial, Managerial und Tax Accounting; erfundene Quellen. Übertragung, älteres Modell, Bildungskontext.
  - Q061: laut Abstract-Zusammenfassung begrenzte Genauigkeit und begrenztes Kontextgedächtnis von Foundation-LLMs in spezialisierten Prüfungsdomänen.
- **Agentenspezifische Risiken:** [H] Sapkota u. a. 2025: Halluzination, Fragilität, emergentes Verhalten, Koordinationsfehler. [H] Chan u. a. 2023: Schäden nehmen mit dem Grad der Agentur zu.
- **Erklärbarkeit:** Q057 behandelt Erklärbarkeit als nötige Fähigkeit.
- **Strukturelle Grenzen im Controlling:** Q059.
- **Datenschutz, Haftung, Compliance (EU AI Act, GoBD, IKS):** keine geprüfte Quelle, Rechercheauftrag an den `source-researcher`.

---

## 4. Abgrenzung zu den Nachbarthemen (Frage 3)

| Nachbarthema | Wo Überschneidung droht | Agentenspezifischer Mehrwert (Stichworte) | Abgrenzungsregel (Vorschlag) |
|---|---|---|---|
| Nr. 3 RPA im Rechnungswesen | Purchase-to-Pay, Record-to-Report, Abstimmungen, Kreditorenrechnungen | Ziel- statt Skriptsteuerung, Ausnahmen und unstrukturierte Eingaben, dynamische Werkzeugwahl; RPA-Bots können Werkzeuge eines Agenten sein [I] | RPA nur als Vergleichsbasis (Q056); RPA-Befunde (z. B. Kokina) nur als gekennzeichnete Übertragung |
| Nr. 5 Predictive Analytics im Controlling | Forecasting, Abweichungsanalyse | Der Agent orchestriert: Prognose auslösen, Abweichung interpretieren, Kommentar vorbereiten, Folgeaktion vorschlagen. Das Prognosemodell ist nur ein Werkzeug [I] | kein Vergleich von Prognoseverfahren |
| Nr. 8 KI im Risikomanagement (Erläuterung im Original abgeschnitten) | Anomalie- und Betrugserkennung, Risikoindikatoren | Unterscheiden: „KI für das Risikomanagement“ (Nr. 8) vs. „Risiken und Governance des Agenteneinsatzes“ (Thema 9, Teil Grenzen/Basis) | Risikomanagement nicht als Hauptanwendungsfall wählen |
| Nr. 2 Treasury / Cash Management | Liquiditätsplanung, Zahlungsverkehr | Agenten mit Freigabestufen bei Zahlungen [I]; die Evidenz ist sehr dünn (nur Q060, konzeptionell) | Treasury höchstens als Randbeispiel |
| Nr. 11 Rollen und Kompetenzen | Kompetenzen als Erfolgsfaktor | neue Aufsichts- und Delegationsrollen gegenüber Agenten (Q052) [I] | Kompetenzen nur als ein Erfolgsfaktor unter mehreren |

Kern des Mehrwerts von Thema 9 [I]: die **Handlungs- und Orchestrierungsebene** (Planung, Werkzeugnutzung, Ausführung) und die daraus folgende **Delegations- und Governancefrage** (Wie viel Autonomie bei welchem Prozessschritt?). Keines der Nachbarthemen deckt das ab.

---

## 5. Mögliche Zuschnitte (keine Entscheidung, keine Forschungsfrage)

| Zuschnitt | Kern (Stichworte) | Begründung aus der Evidenzlage | Risiken | Passung 8–10 S. |
|---|---|---|---|---|
| **Z1 Autonomiegrad als Ordnungsrahmen, übergreifend** | Use Cases über Controlling, Accounting und Treasury nach Funktionstyp × Autonomiestufe ordnen; Erfolgsfaktoren aus einem Architektur- und Governance-Raster ableiten | Die tragfähigste Literatur ist begrifflich und konzeptionell (Q051, Q052, Q054, Q055, Q057); deutlich agentenspezifisch; vermeidet Nr. 3 und Nr. 5 | Abstraktionsgefahr; wenige belegte Finanzbeispiele; Use Cases könnten konzeptionell bleiben | gut, wenn das Raster das Gliederungsprinzip ist |
| **Z2 Rechnungswesen (Abschluss, Kreditoren, interne Kontrollen)** | agentische Prozessschritte, Freigabestufen, Prüfpfad; Erfolgsfaktoren Daten, Kontrollen, Kompetenzen | die meisten agentenspezifischen Prototypen (Q061, Q062, historisch Q058); JETA-Special-Section in Vorbereitung | starke Überschneidung mit Nr. 3; Evidenz überwiegend aus der Abschlussprüfung, also Übertragung | gut, braucht klare RPA-Abgrenzung |
| **Z3 Controlling (Berichtswesen, Abweichungsanalyse, Planung)** | Analyse- und Kommentierungsagenten, Mensch-Agent-Arbeitsteilung, kybernetische Grenzen | Q059 als kritischer Gegenpol, Q062 als Prototyp; Seminar mit Controlling-Fokus (Folie 15, nur Kontext) | kaum agentenspezifische begutachtete Evidenz; Überschneidung mit Nr. 5 | mittel; Gefahr, nur konzeptionell zu argumentieren |
| **Z4 Betriebliche Basis und Governance mit 2–3 exemplarischen Use Cases** | Freigaben, Erklärbarkeit, Datenbasis, Rollen; Use Cases nur exemplarisch | bedient direkt den zweiten Teil von Thema 9 („Schaffung der Basis“); Quellen Q057, Q054, Q052, Q051, Q055 | Abdriften zu Nr. 8 und Nr. 11; der Teil Use Cases wird dünn | gut, wenn Use Cases nicht verloren gehen |
| **Z5 Treasury** | Zahlungsfreigaben, Cash-Positionierung mit Agenten | nur Q060 (konzeptionell, nicht agentenspezifisch) | Evidenz derzeit unzureichend; Überschneidung mit Nr. 2 | **nach derzeitiger Lage nicht empfehlenswert** (Transparenzhinweis) |

---

## 6. Belege mit Prüfstatus

### 6a. Kandidaten (CSV, Q050–Q062)

Für alle gilt: KANDIDAT, Metadaten NICHT_VERIFIZIERT, Peer Review UNKLAR, Zugriff NUR_METADATA. Keine Quelle darf vor der Verifikation in die Evidenzmatrix.

| ID | Kurzbeleg | Typ / Stufe (voraussichtlich) | Rolle | Prüflücke |
|---|---|---|---|---|
| Q050 | Wooldridge/Jennings (1995) | Zeitschriftenartikel, Stufe 1 | klassische Agentendefinition | DOI; Merkmalsliste nur sekundär gesehen; HTML-Volltext auf der Autorenseite (Student prüfen) |
| Q051 | Parasuraman/Sheridan/Wickens (2000) | Zeitschriftenartikel, Stufe 1 | Automatisierungsstufen, Human-in-the-loop | Vornamen; 10-Stufen-Skala nicht sicher aus diesem Artikel |
| Q052 | Baird/Maruping (2021) | Zeitschriftenartikel (MISQ), Stufe 1 | Delegation an agentische IS-Artefakte | Vorname Maruping |
| Q053 | Wang u. a. (2024) | Zeitschriftenartikel, Stufe 1 | LLM-Agent-Architektur (Profil, Gedächtnis, Planung, Aktion) | Autorenliste; Journalfassung statt Preprint zitieren |
| Q054 | Li/Reinhard/Leimeister (2026) | Zeitschriftenartikel (BISE-Catchword), Stufe 1 falls begutachtet | agentische KI im Unternehmen | Begutachtung von Catchwords; die sechs Fähigkeiten sind unbekannt |
| Q055 | Allmendinger u. a. (2026) | Zeitschriftenartikel (Electronic Markets), Stufe 1 falls begutachtet | Fünf-Schichten-Architektur für Multi-Agenten-KI | Rubrik, Begutachtung, Heft |
| Q056 | Chakraborti u. a. (2020) | Konferenzbeitrag (BPM-Forum, LNBIP), Stufe 1 falls begutachtet | Entwicklung von RPA zu IPA | Autorenliste, Band, genauer Titel |
| Q057 | Calvanese u. a. (2026) | Zeitschriftenartikel (Information Systems), Stufe 1 | framed autonomy, Governance | Verlag aus dem DOI-Präfix abgeleitet |
| Q058 | Chou/Du/Lai (2007) | Zeitschriftenartikel (DSS), Stufe 1 | historisches Multi-Agenten-System im Auditing | Vornamen, DOI |
| Q059 | Losbichler/Lehner (2021) | Zeitschriftenartikel (JAAR), Stufe 1 | Grenzen von KI im Controlling | – |
| Q060 | Polák u. a. (2019, online first) | Zeitschriftenartikel (AI & Society), Stufe 1 | Treasury, konzeptionell | Jahr und Heft der Druckfassung |
| Q061 | Xiong/Han/Zhang (2025) | Zeitschriftenartikel (JETA), Stufe 1 | LLM-Audit-Agent, Prototyp | genauer Titel (aus URL-Slug rekonstruiert), Band/Heft |
| Q062 | Resende (2025) | Zeitschriftenartikel (MDPI FinTech), Stufe 1 falls Begutachtung akzeptiert | Agent vs. GPT vs. manuell | Qualität des Peer Reviews, Design |

### 6b. Ungeprüfte Hinweise (NICHT_VERIFIZIERT, nicht in der CSV, um die Obergrenze von ca. 12 einzuhalten)

- **Sapkota/Roumeliotis/Karkee:** „AI Agents vs. Agentic AI: A Conceptual Taxonomy, Applications and Challenges“, laut Treffer Information Fusion, DOI 10.1016/j.inffus.2025.103599. Es gibt arXiv-Fassungen v1–v5; die Journalfassung ist zu prüfen.
- **Holldack/Banh/Strobel (2026):** „Agentic information systems“, Electronic Markets 36, DOI 10.1007/s12525-025-00861-0. Archetypen sowie Risiken auf individueller, organisationaler und gesellschaftlicher Ebene.
- **Feuerriegel/Hartmann/Janiesch/Zschech (2024):** „Generative AI“, BISE 66(1), DOI 10.1007/s12599-023-00834-7. Nützlich für die Abgrenzung von GenAI.
- **van der Aalst/Bichler/Heinzl (2018):** „Robotic Process Automation“, BISE 60(4), Editorial. RPA-Definition; laut Treffer wird darin eine Gartner-Definition zitiert, die Herkunft ist also zu beachten.
- **Chan u. a. (2023):** „Harms from Increasingly Agentic Algorithmic Systems“, FAccT ’23, DOI laut arXiv 10.1145/3593013.3594033.
- **Gu/Schreyer/Moffitt/Vasarhelyi (2024):** „Artificial intelligence co-piloted auditing“, IJAIS 54, 100698, DOI 10.1016/j.accinf.2024.100698.
- **Leitner-Hanetseder/Lehner/Eisl/Forstenlechner (2021):** JAAR 22(3), DOI 10.1108/JAAR-10-2020-0201.
- **Kokina/Gilleran/Blanchette (Proulx)/Stoddard (2021):** Accounting Horizons 35(1), DOI laut AAA 10.2308/HORIZONS-19-145. Nur als RPA-Übertragung.
- **Wood u. a. (2023):** Issues in Accounting Education 38(4). Gegenbefund zur Zuverlässigkeit von GenAI.
- **„Virtual auditing agents: the EDGAR Agent challenge“:** Decision Support Systems, ca. 2000. Autoren per Suche nicht bestätigt; historischer Agentenbezug.
- **Russell/Norvig:** „Artificial Intelligence: A Modern Approach“, 4. Aufl., Pearson. Die ISBN-Angaben der Global Edition sind widersprüchlich.

### 6c. Gesichtet und ausgeschlossen (keine Evidenz)

- arXiv-Preprints, u. a.: Benchmark zur Abschlussprüfung mit LLM-Agent (2506.17282), AuditFlow (2606.03031), „Agentic AI in Finance“-Surveys, „Agentic BPM: Practitioner Perspectives“ (2504.03693).
- Whitepaper und Beratungsmaterial: BCG 2026, FSN 2026.
- Anbieter- und Verbandsumfragen: u. a. PYMNTS, Maximor, Deloitte/IMA, Avalara, IDC. Die Angaben weichen stark voneinander ab; Zahlen bewusst nicht übernommen.
- Fachpresse: Journal of Accountancy, CPA Practice Advisor.
- Masterarbeit auf diplomarbeiten24.de (studentische Arbeit, V S. 15–16).
- Treasury-Review im „International Journal of Management“ (Begutachtungsqualität fraglich).
- Beitrag in einer Zeitschrift des Oikos-Instituts (eoik-2025-0063): nicht geprüft, niedrige Priorität.

---

## 7. Gegenbefunde und Limitationen

1. **Strukturelle Grenzen:** Q059 sieht KI im Controlling aus Komplexitäts- und Kybernetiksicht stark begrenzt. Das spricht gegen hohe Autonomie bei urteilsintensiven Aufgaben. Die Quelle ist nicht agentenspezifisch.
2. **Zuverlässigkeit:** GenAI-Befunde zeigen Fehler bei fachlichen Accounting-Fragen und erfundene Referenzen ([H] Wood 2023). Q061 nennt Genauigkeits- und Kontextgrenzen von LLMs. Beides lässt sich nur als Übertragung auf Agenten verwenden.
3. **Neue agentenspezifische Risiken** durch Koordination mehrerer Agenten und emergentes Verhalten ([H] Sapkota). Die Risiken wachsen mit dem Grad der Agentur ([H] Chan).
4. **Transferproblem:** Die agentenspezifischen Prototypen stammen überwiegend aus der Abschlussprüfung (Q061, Q058, [H] Gu), nicht aus der CFO-Funktion.
5. **Kein Wirkungsnachweis:** Es gibt keine begutachtete Messung von Effizienz oder Effektivität in realen Unternehmen. Q062 ist ein Einzelexperiment mit einer Einzelaufgabe.
6. **Keine wissenschaftlich belegten Zahlen zur Verbreitung.**
7. **Eigene Methodik:** Die Suche bestand aus WebSearch-Läufen, viele davon Known-Item-Suchen nach Titeln aus meinem Vorwissen. Sie ist weder systematisch noch vollständig. Lizenzierte Datenbanken (WISO, EBSCO, Springer Professional, AIS eLibrary) waren nicht durchsuchbar. Die Stufe-2-Suche per WebSearch hat keinen Beitrag aus den Anhang-4-Zeitschriften gefunden. Das belegt nicht, dass es keine gibt.

---

## 8. Offene Forschungs- und Definitionsfragen

- Mindestkriterien, ab denen ein Finanzsystem als „Agent“ gilt (z. B. Werkzeugnutzung plus mehrstufige Planung plus Zielvorgabe). Ist ein Copilot schon ein Agent?
- Wie lassen sich Effizienz und Effektivität von Agenten in der CFO-Funktion operationalisieren? Validierte Kennzahlen habe ich nicht gefunden.
- Verantwortlichkeit und Prüfpfad bei Agentenhandlungen im Rechnungswesen (GoBD, IKS, Abschlussprüfung); Einstufung nach dem EU AI Act; Datenschutz. Juristische und prüfungsnahe Literatur fehlt noch.
- Ist die Übertragung von Befunden aus Abschlussprüfung, RPA und GenAI auf CFO-Agenten zulässig?
- Wurden die älteren Multi-Agenten-Ansätze im Rechnungswesen in der Praxis umgesetzt? Mit den gefundenen Quellen nicht belegbar.
- Verbreitung im DACH-Mittelstand: keine wissenschaftlichen Daten.

---

## 9. Empfehlungen an den Orchestrator

- **Freigabe:** api.crossref.org, doi.org, www.econbiz.de und api.openalex.org in den Netzwerkeinstellungen freigeben, dann Q050–Q062 vom `citation-auditor` verifizieren lassen (DOI-Auflösung, Peer-Review-Nachweise, Heftangaben).
- **Aufträge an den `source-researcher`:**
  - (1) WISO bzw. Springer Professional (vom Studenten mit Hochschulzugang): Controller Magazin, Controlling & Management Review, Controlling (ZfeU), CFO aktuell mit „KI-Agent*“, „agentische KI“, „Agentic AI“.
  - (2) AIS eLibrary: ICIS, ECIS, WI 2025–2026 mit „agentic AI“ plus accounting/finance.
  - (3) Inhaltsverzeichnisse 2025–2026 von JETA (Special Section), IJAIS, Journal of Information Systems und Accounting Horizons.
  - (4) Journalfassung von Sapkota u. a.
  - (5) Rechtliche bzw. GoBD-/IKS-Literatur zu KI-Agenten.
- **Volltexte, die der Student frei lesen kann (legal):**
  - Resende 2025 (MDPI, CC BY).
  - Wooldridge/Jennings 1995 (HTML auf der Autorenseite).
  - Preprint-Fassungen von Wang u. a., Calvanese u. a. und Feuerriegel u. a. nur zum Vorlesen. Zitiert wird die Journalfassung; Abweichungen sind möglich, das Lesen eines Preprints gilt nicht als `VOLLTEXT_GELESEN` der Journalfassung.
- **Freigabebedarf beim Studenten:** Eingrenzung (Z1–Z5), Arbeitsdefinition (D1–D3), Aufnahme von Copilot und Multi-Agenten-Systemen.
- **KI-Protokoll:** Bitte eintragen: Einsatz finance-ai-expert, Begriffsarbeit/Evidenzsichtung, Problem fehlende Verifikationshosts, Status NICHT_VERIFIZIERT.
- **Evidenzmatrix:** derzeit keine Einträge zulässig, weil keine Quelle AUFGENOMMEN ist.

---

## 10. CSV-Blöcke

### literature.csv (Kandidaten)

```csv
source_id,title,authors,year,source_type,publication,publisher,volume_issue_pages,doi,isbn,urn,publication_url,peer_review_status,peer_review_evidence,metadata_status,metadata_evidence,access_level,integrity_flags,finance_area,found_via,decision,decision_reason,added_by,added_date,notes
Q050,Intelligent Agents: Theory and Practice,"Wooldridge, Michael; Jennings, Nicholas",1995,ZEITSCHRIFTENARTIKEL,The Knowledge Engineering Review,,,,,,https://eprints.soton.ac.uk/252102,UNKLAR,,NICHT_VERIFIZIERT,"WebSearch S067: Repositorium eprints.soton.ac.uk/252102, bibsonomy, Autorenseite cs.ox.ac.uk (Treffer nicht abgerufen; Crossref/doi.org in Sitzung nicht erreichbar)",NUR_METADATA,,TECHNIK_GRUNDLAGEN,S067,KANDIDAT,,finance-ai-expert (KI),2026-11-07,"lt. Suchtreffer 10(2), S. 115–152; DOI nicht im Treffer bestätigt. Klassische Agentendefinition (schwache vs. starke Agentur); Merkmalsliste Autonomie/soziale Fähigkeit/Reaktivität/Proaktivität nur über Sekundärzusammenfassung gesehen – am Volltext prüfen. HTML-Fassung auf Autorenseite frei lesbar (Student prüfen)."
Q051,A model for types and levels of human interaction with automation,"Parasuraman; Sheridan; Wickens",2000,ZEITSCHRIFTENARTIKEL,"IEEE Transactions on Systems, Man, and Cybernetics – Part A",IEEE,,10.1109/3468.844354,,,https://bibbase.org/network/publication/parasuraman-sheridan-wickens-amodelfortypesandlevelsofhumaninteractionwithautomation-2000,UNKLAR,,NICHT_VERIFIZIERT,"WebSearch S070: bibbase, manuscript.isc.ac (nicht abgerufen)",NUR_METADATA,,TECHNIK_GRUNDLAGEN,S070,KANDIDAT,,finance-ai-expert (KI),2026-11-07,"lt. Suchtreffer 30(3), S. 286–297; Vornamen nicht aus Treffer bestätigt. Vier Funktionstypen (Informationsaufnahme, Analyse, Entscheidungsauswahl, Ausführung) × Automatisierungsstufen – Raster für Autonomiegrad/Human-in-the-loop. 10-Stufen-Skala nicht sicher aus diesem Artikel."
Q052,The Next Generation of Research on IS Use: A Theoretical Framework of Delegation to and from Agentic IS Artifacts,"Baird, Aaron; Maruping",2021,ZEITSCHRIFTENARTIKEL,MIS Quarterly,,,10.25300/MISQ/2021/15882,,,https://aisel.aisnet.org/misq/vol45/iss1/12,UNKLAR,,NICHT_VERIFIZIERT,"WebSearch S054: aisel.aisnet.org/misq/vol45/iss1/12, econbiz-Record 10012814896 (nicht abgerufen)",NUR_METADATA,,TECHNIK_GRUNDLAGEN,S054,KANDIDAT,,finance-ai-expert (KI),2026-11-07,"lt. Suchtreffer 45(1), S. 315–341; Vorname Maruping prüfen. Delegationsrahmen Mensch–agentisches IS-Artefakt (Attribute endowments/preferences/roles; Mechanismen appraisal/distribution/coordination) – Theorielinse für Freigabe- und HITL-Design."
Q053,A survey on large language model based autonomous agents,"Wang, Lei; u. a.",2024,ZEITSCHRIFTENARTIKEL,Frontiers of Computer Science,,,10.1007/s11704-024-40231-1,,,https://link.springer.com/doi/10.1007/s11704-024-40231-1,UNKLAR,,NICHT_VERIFIZIERT,"WebSearch S051: academic.hep.com.cn, link.springer.com (nicht abgerufen)",NUR_METADATA,,TECHNIK_GRUNDLAGEN,S051,KANDIDAT,,finance-ai-expert (KI),2026-11-07,"lt. Suchtreffer 18(6), Artikel 186345; vollständige Autorenliste und Verlag ergänzen. Architekturrahmen LLM-Agent: Profil, Gedächtnis, Planung, Aktion. Preprint arXiv 2308.11432 nur zum Lesen, zitiert wird Journalfassung."
Q054,Agentic AI: From Autonomous Agents to Enterprise Agentic AI Systems,"Li, Mahei Manhai; Reinhard, Philipp; Leimeister, Jan Marco",2026,ZEITSCHRIFTENARTIKEL,Business & Information Systems Engineering,,,10.1007/s12599-026-01009-w,,,,UNKLAR,,NICHT_VERIFIZIERT,"WebSearch S052, S053: Institutsmeldung iwi.unisg.ch (Juli 2026), ESM-Datei media.springernature.com (nicht abgerufen)",NUR_METADATA,,TECHNIK_GRUNDLAGEN,S052,KANDIDAT,,finance-ai-expert (KI),2026-11-07,"Catchword-Beitrag – Begutachtungsverfahren prüfen. Grenzt agentische KI von klassischen autonomen Agenten und Multi-Agenten-Systemen ab; lt. Meldung sechs Fähigkeiten (nicht einzeln bekannt), Unternehmensbeispiel mit mehreren Agenten, Agenda Design/Governance/Mensch-KI-Zusammenarbeit/Plattform-Ökosysteme. Namensform Mahei Li vs. Mahei Manhai Li prüfen."
Q055,Multi-Agent AI,"Allmendinger, Simeon; Bonenberger, Lukas; Endres, Kathrin; Fetzer, Dominik; Gimpel, Henner; Kühl, Niklas",2026,ZEITSCHRIFTENARTIKEL,Electronic Markets,Springer,,10.1007/s12525-025-00862-z,,,https://eref.uni-bayreuth.de/id/eprint/93903/,UNKLAR,,NICHT_VERIFIZIERT,"WebSearch S052, S077, S081: Crossref-Link in Trefferliste (nicht abrufbar), Repositorium eref.uni-bayreuth.de (nicht abgerufen)",NUR_METADATA,,TECHNIK_GRUNDLAGEN,S052,KANDIDAT,,finance-ai-expert (KI),2026-11-07,"lt. Suchtreffer Bd. 36 (Heft 1?); Rubrik und Begutachtung prüfen; Schreibweise Multi-agent/Multi-Agent prüfen. Fünf Schichten: Foundation Model, datenzentrierte Wahrnehmung und Aktion, dynamische Orchestrierung, agentenintegrierter Workflow, Interaktionsschnittstelle."
Q056,From Robotic Process Automation to Intelligent Process Automation,"Chakraborti; u. a.",2020,KONFERENZBEITRAG,Business Process Management: Blockchain and Robotic Process Automation Forum (Lecture Notes in Business Information Processing),Springer,,10.1007/978-3-030-58779-6_15,,,https://www.bibsonomy.org/bibtex/f80a49482f80c3099e96d4908913db86,UNKLAR,,NICHT_VERIFIZIERT,"WebSearch S064: bibsonomy, academia.edu, arXiv 2007.13257 mit Kommentar BPM 2020 RPA Forum (nicht abgerufen)",NUR_METADATA,,TECHNIK_GRUNDLAGEN,S064,KANDIDAT,,finance-ai-expert (KI),2026-11-07,"lt. Suchtreffer S. 215–228; LNBIP-Bandnummer, vollständige Autorenliste und exakter Titel (arXiv-Fassung mit Zusatz Emerging Trends) prüfen. Überblick RPA zu IPA (RPA ergänzt um KI/ML)."
Q057,Agentic Business Process Management: A Research Manifesto,"Calvanese, Diego; Casciani, Angelo; De Giacomo, Giuseppe; Dumas, Marlon; Fournier, Fabiana; Kampik, Timotheus; La Malfa, Emanuele; Limonad, Lior; Marrella, Andrea; Metzger, Andreas; Montali, Marco; Amyot, Daniel; Fettke, Peter; Polyvyanyy, Artem; Rinderle-Ma, Stefanie; Sardiña, Sebastian; Tax, Niek; Weber, Barbara",2026,ZEITSCHRIFTENARTIKEL,Information Systems,Elsevier,,10.1016/j.is.2026.102738,,,https://portal.fis.tum.de/en/publications/agentic-business-process-management-a-research-manifesto/,UNKLAR,,NICHT_VERIFIZIERT,"WebSearch S066, S068: TUM-Portal, Publikationsliste inf.unibz.it, arXiv 2603.18916 (nicht abgerufen)",NUR_METADATA,,TECHNIK_GRUNDLAGEN,S066,KANDIDAT,,finance-ai-expert (KI),2026-11-07,"lt. Suchtreffer Bd. 140, Artikel 102738 (online 1.8.2026 lt. TUM-Portal); Verlag aus DOI-Präfix abgeleitet. Konzeptionell (Dagstuhl-Seminar). Fähigkeiten: framed autonomy, Erklärbarkeit, conversational actionability, Selbstmodifikation – Rahmen für begrenzte Autonomie und Governance in Prozessen."
Q058,Continuous auditing with a multi-agent system,"Chou; Du; Lai",2007,ZEITSCHRIFTENARTIKEL,Decision Support Systems,,,,,,https://iaorifors.com/paper/58200,UNKLAR,,NICHT_VERIFIZIERT,"WebSearch S055, S076: IAOR-Eintrag, datalearner-Listing, Literaturverzeichnis eines Folgebeitrags lt. Treffer (nicht abgerufen)",NUR_METADATA,,ACCOUNTING,S055,KANDIDAT,,finance-ai-expert (KI),2026-11-07,"lt. Suchtreffer 42(4), S. 2274–2292; Vornamen und DOI fehlen. Historisches Multi-Agenten-System: agentenbasiertes Continuous-Audit-Modell ABCAM (mobile Agenten, fünf Szenarien). Prüfungskontext – für CFO-Funktion nur Begriffsgeschichte/Übertragung. Vorläufer: Konferenzfassung ICEB 2004."
Q059,Limits of artificial intelligence in controlling and the ways forward: a call for future accounting research,"Losbichler, Heimo; Lehner, Othmar M.",2021,ZEITSCHRIFTENARTIKEL,Journal of Applied Accounting Research,Emerald,,10.1108/JAAR-10-2020-0207,,,https://emerald.com/insight/content/doi/10.1108/JAAR-10-2020-0207/full/html,UNKLAR,,NICHT_VERIFIZIERT,"WebSearch S063: Emerald-Seite, econbiz-Record 10012540486, Repositorien Hanken und FH OÖ (nicht abgerufen)",NUR_METADATA,,CONTROLLING,S063,KANDIDAT,,finance-ai-expert (KI),2026-11-07,"lt. Suchtreffer 22(2), S. 365–382. Konzeptionell (semi-systematisches Review plus validierte Forschungsfragen). Drei Grenzen: Bremermann-Grenze, begrenzte Erfassbarkeit/Steuerbarkeit komplexer Systeme, Verzerrungen in der Mensch-Maschine-Komplementarität – nicht agentenspezifisch, Gegenposition. Zugang über Hochschule prüfen."
Q060,"""Intelligent"" finance and treasury management: what we can expect","Polák, Petr; Nelischer, Christof; Guo, Haochen; Robertson, David C.",2019,ZEITSCHRIFTENARTIKEL,AI & Society,Springer,,10.1007/s00146-019-00919-6,,,https://dspace.vsb.cz/handle/10084/138970,UNKLAR,,NICHT_VERIFIZIERT,"WebSearch S058: DSpace-Record VŠB-TU Ostrava (nicht abgerufen)",NUR_METADATA,,TREASURY,S058,KANDIDAT,,finance-ai-expert (KI),2026-11-07,"Online-first 2019 lt. Repositorium (S. 1–12); Jahrgang/Heft der Druckfassung und damit Zitierjahr prüfen. Konzeptionell; Stichworte Finance and Treasury 4.0, RPA, Machine Learning; nicht agentenspezifisch."
Q061,Design AI Agent for Auditing: Applying Large Language Models (LLMs),"Xiong, Fangbing; Han, Quanhong; Zhang, Chengning",2025,ZEITSCHRIFTENARTIKEL,Journal of Emerging Technologies in Accounting,American Accounting Association,,10.2308/jeta-2024-041,,,,UNKLAR,,NICHT_VERIFIZIERT,"WebSearch S059, S062: Index-Eintrag ai.updf.com, Zitat in IJACSA 2026 (nicht abgerufen)",NUR_METADATA,,ACCOUNTING,S059,KANDIDAT,,finance-ai-expert (KI),2026-11-07,"Titelzeichensetzung aus URL-Slug rekonstruiert – exakt prüfen; Band/Heft fehlen. Prototypisch: LLM-Audit-Agent mit RAG auf private Wissensbasen, Workflows mit Anfrageklassifikation und Multi-Agenten-Koordination, Prompts mit Prüfungsmethodik; Evaluation lt. Abstract-Zusammenfassung erst geplant. Prüfungskontext – Übertragung auf CFO-Funktion kennzeichnen."
Q062,AI Agents and No-Code Tools in Accounting: A Case Study,"Resende, Miguel",2025,ZEITSCHRIFTENARTIKEL,FinTech,MDPI,,10.3390/fintech4040065,,,https://www.econbiz.de/Record/ai-agents-and-no-code-tools-in-accounting-a-case-study-resende-miguel/10015547405,UNKLAR,,NICHT_VERIFIZIERT,"WebSearch S056, S060: econbiz-Record 10015547405, MDPI-PDF (nicht abgerufen)",NUR_METADATA,,ACCOUNTING,S056,KANDIDAT,,finance-ai-expert (KI),2026-11-07,"lt. Suchtreffer Bd. 4 (Heft 4), Artikel 65, 14 S.; Open Access CC BY 4.0. Vergleich manuell vs. spezialisiertes GPT vs. KI-Agent (GPT plus No-Code-Automatisierung) bei vertikaler GuV-Analyse; lt. Suchzusammenfassung 150 experimentelle Fälle, größter Effizienzgewinn beim Agenten – Design und Agentenbegriff am Volltext prüfen; Einzelautor; Begutachtungsqualität MDPI prüfen."
```

### search_log.csv

```csv
search_id,search_date,executed_by,database,interface,search_string,filters,result_count,result_count_basis,export_path,notes
S050,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"""agentic AI"" definition conceptual taxonomy AI agents vs agentic AI journal article 2025",,10,ZURUECKGEGEBENE_TREFFER,,"Begriffsarbeit; fast nur arXiv-Spiegel zu Sapkota u. a. (Journalfassung Information Fusion lt. Treffer) – Hinweis, nicht in CSV"
S051,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"""large language model based autonomous agents"" survey Frontiers of Computer Science planning memory action",,10,ZURUECKGEGEBENE_TREFFER,,"Known-Item-Suche (Titel aus Vorwissen des KI-Agenten); Q053"
S052,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Business & Information Systems Engineering catchword ""agentic AI"" OR ""AI agents"" 2025",,10,ZURUECKGEGEBENE_TREFFER,,"Q054 und Q055 gefunden; übrige Treffer Presse/Anbieter/Preprint"
S053,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Li Reinhard Leimeister ""Agentic AI: From Autonomous Agents to Enterprise Agentic AI Systems"" Business & Information Systems Engineering DOI",,10,ZURUECKGEGEBENE_TREFFER,,"Metadatenabgleich Q054 (DOI lt. Institutsmeldung)"
S054,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Baird Maruping 2021 MIS Quarterly ""agentic IS artifacts"" delegation theoretical framework",,10,ZURUECKGEGEBENE_TREFFER,,"Known-Item-Suche; Q052"
S055,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"""intelligent agents"" accounting auditing multi-agent system journal ""continuous auditing"" agent-based 2000s",,10,ZURUECKGEGEBENE_TREFFER,,"ältere Agenten-/MAS-Literatur Accounting/Auditing; Q058; Hinweis EDGAR-Agent (DSS ca. 2000); JETA-Call Agentic AI (keine Quelle)"
S056,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"""agentic AI"" accounting journal article 2025 2026 ""Journal of Emerging Technologies in Accounting"" OR ""International Journal of Accounting Information Systems"" OR ""Accounting Horizons""",,10,ZURUECKGEGEBENE_TREFFER,,"keine Artikel in den drei Journals; JETA-Call for Papers; Q062; Rest Fachpresse"
S057,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"""AI agents"" OR ""agentic AI"" ""management accounting"" OR controlling peer-reviewed study finance function CFO",,10,ZURUECKGEGEBENE_TREFFER,,"keine begutachtete Studie; nur Anbieter-/Beratungsumfragen und Whitepaper (ausgeschlossen)"
S058,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Polak Nelischer Guo Robertson ""Intelligent"" finance and treasury management: what we can expect AI & Society",,10,ZURUECKGEGEBENE_TREFFER,,"Known-Item-Suche; Q060; übrige Treffer Fachpresse/Anbieter"
S059,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"LLM ""multi-agent"" OR ""AI agent"" auditing accounting prototype ""International Journal of Accounting Information Systems"" OR ""Journal of Information Systems"" 2024 2025",,10,ZURUECKGEGEBENE_TREFFER,,"Q061; mehrere arXiv-Preprints (ausgeschlossen)"
S060,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Resende ""AI agents and no-code tools in accounting: a case study"" FinTech MDPI 2025",,10,ZURUECKGEGEBENE_TREFFER,,"Metadatenabgleich Q062"
S061,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Gu Schreyer Moffitt Vasarhelyi ""Artificial intelligence co-piloted auditing"" International Journal of Accounting Information Systems",,10,ZURUECKGEGEBENE_TREFFER,,"Known-Item-Suche; Hinweis Gu u. a. 2024 (nicht in CSV)"
S062,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"""Design AI Agent for Auditing"" large language models Journal of Emerging Technologies in Accounting Xiong Han",,10,ZURUECKGEGEBENE_TREFFER,,"Metadatenabgleich Q061"
S063,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Losbichler Lehner ""Limits of artificial intelligence in controlling and the ways forward"" Journal of Applied Accounting Research",,10,ZURUECKGEGEBENE_TREFFER,,"Known-Item-Suche; Q059"
S064,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"van der Aalst Bichler Heinzl ""Robotic Process Automation"" Business & Information Systems Engineering 2018 definition; Chakraborti ""From Robotic Process Automation to Intelligent Process Automation"" BPM 2020",,10,ZURUECKGEGEBENE_TREFFER,,"Known-Item-Suche; Q056; Hinweis van der Aalst u. a. 2018 (nicht in CSV)"
S065,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Leitner-Hanetseder Lehner Eisl Forstenlechner ""A profession in transition: actors, tasks and roles in AI-based accounting"" Journal of Applied Accounting Research",,10,ZURUECKGEGEBENE_TREFFER,,"Known-Item-Suche; Hinweis (nicht in CSV, Überschneidung Nr. 11)"
S066,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Dumas ""AI-augmented Business Process Management Systems: A Research Manifesto"" ACM Transactions on Management Information Systems framed autonomy",,10,ZURUECKGEGEBENE_TREFFER,,"Known-Item-Suche mit falscher Venue-Annahme (TMIS nicht bestätigt; 2022er Fassung nur als arXiv gefunden); dabei Q057 gefunden"
S067,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Wooldridge Jennings 1995 ""Intelligent agents: theory and practice"" Knowledge Engineering Review autonomy reactivity pro-activeness social ability",,10,ZURUECKGEGEBENE_TREFFER,,"Known-Item-Suche; Q050"
S068,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"""Agentic Business Process Management: A Research Manifesto"" Information Systems 2026 102738 authors",,10,ZURUECKGEGEBENE_TREFFER,,"Metadatenabgleich Q057"
S069,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Feuerriegel Hartmann Janiesch Zschech ""Generative AI"" Business & Information Systems Engineering 2024 66 111-126",,10,ZURUECKGEGEBENE_TREFFER,,"Known-Item-Suche; Hinweis (nicht in CSV)"
S070,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Parasuraman Sheridan Wickens 2000 ""A model for types and levels of human interaction with automation"" IEEE Transactions Systems Man Cybernetics",,10,ZURUECKGEGEBENE_TREFFER,,"Known-Item-Suche; Q051"
S071,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"""generative AI"" management accountants OR controllers interview OR survey study 2024 2025 journal ""management accounting"" adoption empirical",,10,ZURUECKGEGEBENE_TREFFER,,"nur Beratungs-/Verbandsumfragen und Presse (ausgeschlossen); keine begutachtete Studie"
S072,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Wood et al. 2023 ""The ChatGPT Artificial Intelligence Chatbot: How Well Does It Answer Accounting Assessment Questions?"" Issues in Accounting Education",,10,ZURUECKGEGEBENE_TREFFER,,"Known-Item-Suche; Gegenbefund GenAI (Hinweis, nicht in CSV)"
S073,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"corporate treasury ""artificial intelligence"" OR ""machine learning"" cash management peer-reviewed journal article liquidity forecasting nonfinancial firms",,10,ZURUECKGEGEBENE_TREFFER,,"keine begutachtete Treasury-Studie; Review in International Journal of Management (Begutachtungsqualität fraglich, nicht verfolgt); Rest Bank-/Fachpresse"
S074,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"""KI-Agenten"" Controlling OR Finanzbereich OR Rechnungswesen ""Controller Magazin"" OR ""Controlling & Management Review"" OR ""CFO aktuell"" 2025 2026",,16,ZURUECKGEGEBENE_TREFFER,,"Stufe-2-Suche erfolglos: keine Beiträge der Anhang-4-Zeitschriften; nur Seminare, Anbieter, Presse, eine Masterarbeit (ausgeschlossen) – Datenbanksuche WISO/Springer Professional nötig"
S075,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"""agentic AI"" OR ""LLM agents"" ""financial planning and analysis"" OR budgeting OR ""financial close"" OR ""accounts payable"" peer-reviewed conference OR journal 2025",,10,ZURUECKGEGEBENE_TREFFER,,"keine begutachtete Prozessstudie; Preprints, Anbieterblogs; ein konzeptioneller Beitrag in Oikos-Institut-Journal (nicht geprüft)"
S076,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Chou Du Lai ""Continuous auditing with a multi-agent system"" Decision Support Systems 2007 42(4) 2274",,10,ZURUECKGEGEBENE_TREFFER,,"Metadatenabgleich Q058"
S077,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Electronic Markets 2025 ""10.1007/s12525-025-00862"" agent",,10,ZURUECKGEGEBENE_TREFFER,,"Identifikation Q055; Hinweis Holldack u. a. 2026 (nicht in CSV)"
S078,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Chan et al. ""Harms from Increasingly Agentic Algorithmic Systems"" FAccT 2023 underspecification goal-directedness long-term planning",,10,ZURUECKGEGEBENE_TREFFER,,"Known-Item-Suche; Hinweis (nicht in CSV)"
S079,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Kokina Gilleran Blanchette Stoddard ""Accountant as digital innovator: Roles and competencies in the age of automation"" Accounting Horizons",,10,ZURUECKGEGEBENE_TREFFER,,"Known-Item-Suche; RPA-Rollen (Übertragung, Überschneidung Nr. 3/11) – Hinweis"
S080,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Holldack ""Agentic information systems"" Electronic Markets OR Business & Information Systems Engineering 2025 2026",,10,ZURUECKGEGEBENE_TREFFER,,"Metadatenabgleich Hinweis Holldack u. a. 2026"
S081,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Allmendinger ""Multi-agent AI"" Electronic Markets fundamentals dynamic orchestration agent-integrated workflow",,10,ZURUECKGEGEBENE_TREFFER,,"Metadatenabgleich Q055"
S082,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"""agentic AI"" ""finance function"" OR ""corporate finance function"" OR ""CFO"" case study OR interview study peer-reviewed journal 2025 2026 Emerald OR Springer OR Elsevier",,10,ZURUECKGEGEBENE_TREFFER,,"keine begutachtete Fall-/Interviewstudie; Umfragen, Whitepaper, Preprints (ausgeschlossen)"
S083,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"""AI agents"" OR ""agentic AI"" ""internal control"" OR ""audit trail"" OR accountability accounting systems governance journal article 2025 2026",,10,ZURUECKGEGEBENE_TREFFER,,"keine begutachtete Studie; JETA-Call; Anbieter-/Verbandsmaterial (ausgeschlossen)"
S084,2026-11-07,finance-ai-expert (KI),Web-Suchmaschine,WebSearch-Tool,"Russell Norvig ""Artificial Intelligence: A Modern Approach"" 4th edition Pearson ISBN agent definition rational agent",,17,ZURUECKGEGEBENE_TREFFER,,"Known-Item-Suche; ISBN-Angaben Global Edition widersprüchlich – Hinweis, nicht in CSV"
S085,2026-11-07,finance-ai-expert (KI),Crossref REST API,WebFetch-Tool,"query.bibliographic=Agentic AI From Autonomous Agents to Enterprise Agentic AI Systems; rows=5",,,UNBEKANNT,,"Abruf fehlgeschlagen (getaddrinfo ENOTFOUND). Ebenso fehlgeschlagen: api.crossref.org/works/<DOI>, doi.org, www.econbiz.de, api.openalex.org – Hosts in den Netzwerkeinstellungen der Sitzung freigeben"
```

---

## 11. Fundstellen der Suchtreffer (nur Auffinden, keine Belege)

- [IWI HSG – Meldung zum BISE-Catchword (Q054)](https://iwi.unisg.ch/en/newsuebersicht/news-detail/news/catchword-artikel-agentic-ai-from-autonomous-agents-to-enterprise-agentic-ai-systems/)
- [Springer – Wang u. a. 2024 (Q053)](https://link.springer.com/doi/10.1007/s11704-024-40231-1)
- [AIS eLibrary – Baird/Maruping 2021 (Q052)](https://aisel.aisnet.org/misq/vol45/iss1/12)
- [Uni Bayreuth eref – Allmendinger u. a. (Q055)](https://eref.uni-bayreuth.de/id/eprint/93903/)
- [TUM-Portal – Agentic BPM Manifesto (Q057)](https://portal.fis.tum.de/en/publications/agentic-business-process-management-a-research-manifesto/)
- [Bibsonomy – Chakraborti u. a. 2020 (Q056)](https://www.bibsonomy.org/bibtex/f80a49482f80c3099e96d4908913db86)
- [Southampton eprints – Wooldridge/Jennings 1995 (Q050)](https://eprints.soton.ac.uk/252102)
- [bibbase – Parasuraman u. a. 2000 (Q051)](https://bibbase.org/network/publication/parasuraman-sheridan-wickens-amodelfortypesandlevelsofhumaninteractionwithautomation-2000)
- [IAOR – Chou/Du/Lai 2007 (Q058)](https://iaorifors.com/paper/58200)
- [Emerald – Losbichler/Lehner 2021 (Q059)](https://emerald.com/insight/content/doi/10.1108/JAAR-10-2020-0207/full/html)
- [VŠB DSpace – Polák u. a. (Q060)](https://dspace.vsb.cz/handle/10084/138970)
- [Index-Eintrag – Xiong/Han/Zhang 2025 (Q061)](https://ai.updf.com/paper-detail/design-ai-agent-for-auditing-applying-large-language-models-llms-xiong-han-3ba985fa108a0135ad08cad6587632eca6779c54)
- [EconBiz-Record – Resende 2025 (Q062)](https://www.econbiz.de/Record/ai-agents-and-no-code-tools-in-accounting-a-case-study-resende-miguel/10015547405)
- [AAA – JETA Call for Papers Agentic AI (keine Quelle, nur Signal)](https://aaahq.org/portals/0/documents/calls/2026/JETA%20CFP%20Agentic%20AI.pdf)
- [EconBiz-Record – Holldack u. a. (Hinweis)](https://www.econbiz.de/Record/agentic-information-systems-holldack-florian/10015564102)

Relevante Projektdateien (gelesen, nicht verändert):
- /home/user/reyan232/00_admin/seminar_requirements.md
- /home/user/reyan232/01_scope/topic_options.md
- /home/user/reyan232/00_admin/datenmodell.md
- /home/user/reyan232/02_search/search_protocol.md
- /home/user/reyan232/03_sources/literature.csv (leer, nur Kopfzeile)
- /home/user/reyan232/02_search/search_log.csv (leer, nur Kopfzeile)
