# methodology-advisor – Phase 1: Zuschnittsoptionen Thema 9 (2026-11-07)

> Herkunft: KI-generiert (methodology-advisor, 2026-11-07) – nicht zur Abgabe. Ich habe nur gelesen und keine Dateien geschrieben. Eine Webrecherche habe ich nicht durchgeführt. Alles ist ein Vorschlag, nichts ist eine Entscheidung.

> **Hinweis des Orchestrators (2026-11-07):** Q014 ist in `literature.csv` als WIDERSPRUECHLICH geführt (widersprüchliche Verlagsangaben laut source-researcher), Q008 wegen Platzhalterangaben im Crossref-Eintrag. Alle Optionen sind Vorschläge; entschieden hat der Student noch nichts.


## 0. Kurzfazit
- Ich schlage drei Zuschnitte vor:
  - **A** Autonomie- und Delegationsstufen als Brücke zwischen Use Cases und betrieblicher Basis (Controlling und Rechnungswesen)
  - **B** Rechnungswesen-Prozesse mit IKS, Prüfpfad und Freigaben
  - **C** Controlling (Berichtswesen und Abweichungsanalyse) mit seinen Grenzen
- Treasury biete ich nicht als eigenen Zuschnitt an. Beide Agentenberichte stimmen darin überein, dass Stufe 1 dort praktisch leer ist. Hinzu kommt die Überschneidung mit Nr. 2.
- **Empfehlung (keine Entscheidung): Option A.** B ist die Ausweichoption, wenn WISO/EBSCO zusätzliche agentenspezifische Belege aus dem Rechnungswesen und Quellen zu IKS/GoBD liefert. C trägt nur, wenn WISO deutlich mehr Stufe-2-Material bringt.
- Als Review-Typ empfehle ich für alle Optionen ehrlich eine **„strukturierte Literaturrecherche“**, keinen systematischen Review und keinen Scoping Review.
- Der Prüfstand gilt für alle Kandidaten in `03_sources/literature.csv`:
  - Die Metadaten sind per Crossref VERIFIZIERT. Ausnahmen mit Status WIDERSPRUECHLICH sind Q008 und Q014.
  - Der Peer-Review-Status ist überall UNKLAR, der Zugriff überall NUR_METADATA.
  - Alle Inhaltsangaben stammen aus Zusammenfassungen der Suchmaschine, sind also selbst KI-Ausgabe. Meine Bewertung der Forschbarkeit ist deshalb **vorläufig**.

**ID-Zuordnung:** Der finance-ai-expert-Bericht verwendet alte IDs. In der CSV gilt:

| Alte ID (Bericht) | Gültige ID (CSV) |
|---|---|
| Q052 | Q006 |
| Q053 | Q009 |
| Q055 | Q012 |
| Q061 | Q002 |
| Q062 | Q001 |

Ich verwende im Folgenden nur die CSV-IDs.

---

## 1. Freigabestand (aus `00_admin/decision_log.md`)
- **Entschieden:** Thema 9, zweistufiges Quellen-Gate (K2), Zitierstil (K3).
- **Offen:** Eingrenzung des Teilbereichs, Forschungsfrage, Review-Typ, Methodik, Ausschlusscodes (E1–E9 sind nur ENTWURF), Zeitraum und Sprachen.
- Ich behandle nichts davon als entschieden.

---

## 2. Optionen

### Option A – Autonomie- und Delegationsstufen als Ordnungsrahmen (Controlling und Rechnungswesen, übergreifend)
- **Arbeitstitel als Stichwortkette:** KI-Agenten · CFO-Funktion (Controlling, Rechnungswesen) · Autonomie- und Delegationsstufen · Use Cases × betriebliche Voraussetzungen · literaturgestützter Ordnungsrahmen.
- **Herkunft:** entspricht Z1 und dem Kern von Z4 aus dem finance-ai-expert-Bericht. Treasury wäre ausgeschlossen oder höchstens ein einzelnes, gekennzeichnetes Randbeispiel.
- **Fragetyp (Folie 64):** Kritik/Bewertung mit einem gestaltungsorientierten Anteil.
  - Gestaltung heißt hier: Voraussetzungen literaturgestützt ableiten und als eigene Synthese kenntlich machen (L S. 1, Folie 87).
  - Nicht geeignet sind Prognose und Erklärung, weil es keine empirischen Wirkungsdaten gibt.
- **Leitaspekte:**
  1. Konkrete Use Cases nach Funktionstyp und Autonomiegrad einordnen. Funktionstypen nach Q051: Informationsaufnahme, Analyse, Entscheidungsauswahl, Ausführung.
  2. Welche Basis braucht welche Stufe? Kandidaten: Daten- und Wissensbasis, Prozess- und Systemintegration, Freigaben und Kontrollen, Rollen und Kompetenzen.
  3. Evidenzstand je Feld der Matrix sowie Bewertung von Effizienz, Effektivität und Grenzen.
- **Warum forschbar** (Quellen nach Funktion; wo nicht anders angegeben, Stufe-1-Kandidaten):
  - **Rahmen und Begriff** (KONZEPTIONELL/DEFINITION): Q051 Parasuraman u. a. 2000, Q006 Baird/Maruping 2021, Q057 Calvanese u. a. 2026, Q050 Wooldridge/Jennings 1995.
  - **Technik-Einordnung** (LITERATURREVIEW/KONZEPTIONELL): Q009, Q010, Q011, Q012, Q054 sowie Q056 zur Abgrenzung RPA/IPA.
  - **Use Cases** (dünn):
    - Q001: EXPERIMENT_PROTOTYP, Rechnungswesen bzw. Analyse.
    - Q002: Prototyp aus der Abschlussprüfung, nur als Übertragung.
    - Q058: historisches Multi-Agenten-System, nur Begriffsgeschichte.
    - Q059: Controlling, KONZEPTIONELL, als Gegenposition.
    - Stufe 2: Q013, Agentenbezug offen. WISO steht aus.
  - **Erfolgsfaktoren und Risiken:**
    - Q007: KONZEPTIONELL, agentenspezifisch, branchenübergreifend.
    - Q008: empirisch, KI allgemein, nur als Übertragung.
    - Q005: empirisch, KI allgemein, Finanzführungskräfte.
  - **Geprüft:** nur die Metadaten.
  - **Angenommen:** Inhalte und Begutachtung. Besonders offen ist das bei Q054 (BISE-Catchword), Q057 (Manifest), Q010 (IEEE Access) und Q001 (MDPI).
- **Risiken und ehrlicher Umgang:**
  - *Abstraktion bzw. Theoriearbeit ohne Finanzbezug:* Eine Mindestzahl konkreter Use Cases aus Finanzprozessen vorab festlegen. Meine Heuristik, keine Vorgabe: 3–5, jeweils mit Beleg. Die Matrix auf Controlling und Rechnungswesen begrenzen.
  - *Übertragung:* Die Raster aus Human Factors (Q051) und Wirtschaftsinformatik (Q006, Q057) sind nicht finanzspezifisch. Ihre Anwendung als eigene Übertragung kennzeichnen. Q059 als Gegenposition einbauen.
  - *Leere Matrixfelder:* nicht auffüllen, sondern als Befund „keine begutachtete Evidenz“ ausweisen. Das wird dann Teil des Erkenntnisgewinns.
  - *Abhängigkeit von D2 (Agentur graduell):* Die Stufen müssen vorab operationalisiert und begründet sein. Sonst wird die Zuordnung beliebig.
  - *Überschneidung:*
    - Nr. 8: Governance des Agenteneinsatzes ist etwas anderes als Risikomanagement als Anwendungsfall.
    - Nr. 11: Kompetenzen nur als ein Faktor unter mehreren behandeln.
- **Passung zu 8–10 Seiten:** gut, wenn das Raster das Ordnungsprinzip ist. Eine Matrix-Tabelle (ca. ½ Seite) zählt mit. Grobe Orientierung bei ca. 9,5 Seiten:

| Teil | Seiten |
|---|---|
| Einleitung inkl. Methodik | ca. 1–1,25 |
| Hauptteil (≥ ¾) | ca. 7,5 |
| – Begriff und Rahmen | 1,5–2 |
| – eingeordnete Use Cases | 2–2,5 |
| – Voraussetzungen je Stufe | 1,5–2 |
| – Bewertung, Evidenzlücke, Grenzen | 1–1,5 |
| Schluss | ca. 0,5–0,75 |

- **Review-Typ:** strukturierte Literaturrecherche mit Datenbanksuche, gezielter Grundlagenrecherche und Schneeballsuche. Synthese thematisch über eine Konzeptmatrix.
- **Vor der Festlegung in WISO/EBSCO prüfen:**
  - Gibt es agentenspezifische Beiträge (Stufe 1 oder 2) mit einem konkreten Prozess aus Controlling oder Rechnungswesen, die sich einordnen lassen?
  - Gibt es Literatur zu Freigaben und Human-in-the-loop in Finanzprozessen? Zusatzterme: „human-in-the-loop“, „human oversight“, „levels of automation“, Delegation, Freigabe*.
  - Zugang klären: Q006 (MISQ über EBSCO), Q051 (IEEE), Q057 (Elsevier).

### Option B – Rechnungswesen: agentenspezifische Use Cases in abgegrenzten Prozessen und Basis (Daten, IKS/Prüfpfad, Freigaben)
- **Arbeitstitel als Stichwortkette:** KI-Agenten · Rechnungswesen (2–3 ausgewählte Prozesse, z. B. abschlussnahe Analyse, Abstimmungen, Kreditoren) · Abgrenzung RPA/IPA/GenAI · Use Cases · Datenbasis, interne Kontrollen und Prüfpfad, Freigabestufen.
- **Herkunft:** entspricht Z2 und weitgehend der Empfehlung des source-researcher.
- **Fragetyp:** Beschreibung und Kritik/Bewertung.
- **Leitaspekte:**
  1. Welche Aufgaben im Rechnungswesen sind agentenspezifisch und nicht mit RPA lösbar? Merkmale: Planung, Werkzeugwahl, Ausnahmen, unstrukturierte Belege.
  2. Voraussetzungen: Daten, IKS und Prüfpfad, Freigaben, Kompetenzen.
  3. Lassen sich Prototypen aus der Prüfung auf CFO-interne Prozesse übertragen?
- **Warum forschbar:**
  - **Use Cases:**
    - Q001: einziger agentenspezifischer, CFO-naher Fall (EXPERIMENT_PROTOTYP).
    - Q002: Prototyp aus der Prüfung (Übertragung oder Ausschluss nach E1).
    - Q003: Copilot, nur zur Abgrenzung.
    - Q004: GenAI in der internen Revision bei Uniper, realer Fall, als Kontrast.
    - Q058: historisch.
  - **Akzeptanz:** Q005 (empirisch, KI in der Finanzberichterstattung).
  - **Abgrenzung zu RPA:** Q056.
  - **Erfolgsfaktoren konzeptionell:** Q006, Q051, Q057, Q007, Q008.
  - **Lücken:**
    - Keine geprüfte Quelle zu IKS, GoBD oder Prüfpfad.
    - Keine Stufe-1-Prozessstudie zu Abschluss oder Kreditoren (S075 und S083 ohne Ergebnis).
    - Nicht in der CSV, NICHT_VERIFIZIERT: Kokina u. a. 2021, van der Aalst u. a. 2018, Leitner-Hanetseder u. a. 2021.
- **Risiken und ehrlicher Umgang:**
  - *Überschneidung mit Nr. 3 (RPA im Rechnungswesen) hoch:* RPA nur als Vergleichsbasis verwenden. Den Merkmalskatalog (D1/D4) strikt anwenden und Grenzfälle offenlegen.
  - *Übertragung von der Prüfung auf die CFO-Funktion:* Wird E1 streng ausgelegt, bleibt agentenspezifisch nur Q001 übrig, und die Option kippt.
  - *Typische Prozesse (Kreditoren, Abschluss):* Belege gibt es bisher nur aus Anbietermaterial, das ausgeschlossen ist. Beispiele kämen also nur aus Stufe 2, und Stufe 2 ist nie alleiniger Beleg.
  - *Regulatorik (IKS/GoBD):* Dafür wäre deutsche Fachliteratur nötig (NWB, beck-online). Der Betrieb und Betriebs-Berater stehen in Anhang 4, wären also Stufe 2. Der Datenbankzugang ist offen.
- **Passung zu 8–10 Seiten:** gut bei 2–3 Prozessen. Wegen Nr. 3 braucht die Abgrenzung mehr Platz. Grobe Orientierung:

| Teil | Seiten |
|---|---|
| Einleitung inkl. Methodik | ca. 1–1,25 |
| Hauptteil (≥ ¾) | ca. 7,5 |
| – Begriff und Abgrenzung RPA/IPA/GenAI | 1,5–2 |
| – Use Cases | 2–2,5 |
| – Voraussetzungen | ca. 2 |
| – Bewertung | 1–1,5 |
| Schluss | ca. 0,5–0,75 |

- **Review-Typ:** strukturierte Literaturrecherche, zusätzlich NWB und beck-online für den regulatorischen Rahmen.
- **Vor der Festlegung in WISO/EBSCO prüfen:**
  - Gibt es agentenspezifische Stufe-1-Beiträge über Q001/Q002 hinaus? Zu prüfen: ob die JETA-Sonderrubrik „Agentic AI“ schon erschienen ist, außerdem IJAIS, Journal of Information Systems und Accounting Horizons 2025–2026.
  - Stufe 2: Der Betrieb, Betriebs-Berater, ZfC und Controller Magazin mit „KI-Agent*“ AND (Buchhaltung OR Abschluss OR Kreditoren).
  - GoBD/IKS in Verbindung mit KI (NWB, beck-online).
  - **Go/No-Go (Heuristik):** Ohne weitere agentenspezifische Belege für CFO-interne Prozesse lässt sich B kaum von Nr. 3 abgrenzen.

### Option C – Controlling: Analyse-, Kommentierungs- und Orchestrierungsagenten, Potenziale gegenüber strukturellen Grenzen
- **Arbeitstitel als Stichwortkette:** KI-Agenten · Controlling (Berichtswesen, Abweichungsanalyse und -kommentierung, Forecast-Orchestrierung) · Arbeitsteilung Mensch–Agent · Potenziale vs. Grenzen · Voraussetzungen.
- **Herkunft:** entspricht Z3.
- **Fragetyp:** Kritik/Bewertung, ergänzt um Beschreibung.
- **Leitaspekte:**
  1. Welche Aufgaben im Berichts- und Analyseprozess könnten Agenten orchestrieren? Prognosemodelle nur als Werkzeug behandeln.
  2. Grenzen bei urteilsintensiven Steuerungsaufgaben (Q059).
  3. Voraussetzungen: Daten, Steuerungsmodell, Akzeptanz, Freigaben.
- **Warum forschbar (schwächste Basis der drei Optionen):**
  - Stufe 1 im Controlling gibt es nur mit Q059 (KONZEPTIONELL, nicht agentenspezifisch).
  - Q001 trägt nur, wenn die vertikale GuV-Analyse als controllingnah gilt. Diese Einordnung ist strittig (siehe Abschnitt 8).
  - Erfolgsfaktoren nur als Übertragung: Q005, Q006, Q051, Q008.
  - Stufe 2:
    - Q013: CMR 69(5), Agentenbezug offen.
    - Q014: Praxisfachbuch mit ungeklärter Stufe und widersprüchlichem Verlag.
  - Ausgeschlossen: Q018 (Working Paper) und Q021 (Masterarbeit).
- **Risiken und ehrlicher Umgang:**
  - *Stärkste Abhängigkeit von Stufe 2:* Kernaussagen dürfen nicht allein auf Stufe 2 beruhen. Verallgemeinerungen daher vorsichtig formulieren und Unsicherheit offen benennen.
  - *Überschneidung mit Nr. 5:* Prognoseverfahren ausklammern.
  - *Abgrenzung zu GenAI- und Copilot-Kommentierung (D5) schwierig:* Viele Beiträge zu „KI im Controlling“ behandeln GenAI allgemein, fallen also unter E3.
- **Passung zu 8–10 Seiten:** mittel, und nur bei positivem WISO-Befund. Grobe Orientierung:

| Teil | Seiten |
|---|---|
| Einleitung inkl. Methodik | ca. 1–1,25 |
| Hauptteil (≥ ¾) | ca. 7,5 |
| – Begriff | ca. 1,5 |
| – Use Cases | ca. 2 |
| – Grenzen | ca. 1,5 |
| – Voraussetzungen | 1,5–2 |
| – Bewertung | ca. 1 |
| Schluss | ca. 0,5–0,75 |

- **Review-Typ:** strukturierte Literaturrecherche mit Schwerpunkt Stufe 2 in WISO. Die Rolle von Stufe 2 muss im Methodikteil transparent werden.
- **Vor der Festlegung in WISO prüfen:**
  - Stufe 2: Controller Magazin, CMR, Controlling (ZfC) und CFO aktuell, 2024–2026, mit „KI-Agent*“, „agentische KI“, „Agentic AI“. Copilot* zusätzlich mitsuchen, um diese Treffer gegen E3 zu screenen.
  - Stufe 1: Journal of Management Control, Management Accounting Research, JAAR, QRAM und Journal of Accounting & Organizational Change mit LLM- oder Agentenbezug.
  - Den Volltext von Q013 auf Agentenbezug prüfen.
  - **Go/No-Go (Heuristik):** mehrere Stufe-2-Beiträge mit agentischen Merkmalen und mindestens eine weitere Stufe-1-Quelle zu LLMs oder Agenten im Controlling.

### Bewusst nicht angeboten
- **Treasury (Z5):**
  - Q060 ist konzeptionell und nicht agentenspezifisch.
  - Q017 betrifft Banken und ist ein Working Paper, also ausgeschlossen.
  - Dazu kommt die Überschneidung mit Nr. 2.
- **Z4 (Basis und Governance mit exemplarischen Use Cases):** Die Quellenbasis ist dieselbe wie bei A. Außerdem droht der Use-Case-Teil zu verkümmern, obwohl Thema 9 beide Teile verlangt. Ich habe Z4 deshalb als Gewichtungsvariante in A aufgenommen.

---

## 3. Vergleichstabelle

| Kriterium | A Autonomierahmen | B Rechnungswesen | C Controlling |
|---|---|---|---|
| Agentenspezifischer Mehrwert gegenüber den Nachbarthemen | hoch (Handlungs- und Delegationsebene) | mittel (RPA-Nähe) | mittel (Nähe zu GenAI und Nr. 5) |
| Verknüpfung Use Cases ↔ Basis (beide Teile von Thema 9) | strukturell eingebaut | nebeneinander | nebeneinander |
| Stufe-1-Basis heute (nur Metadaten geprüft) | Rahmen und Technik gut, Use Cases dünn | Use Cases dünn, nur 1 CFO-naher Agent (Q001) | sehr dünn (Q059, nicht agentenspezifisch) |
| Abhängigkeit vom WISO/EBSCO-Ergebnis | gering bis mittel | mittel bis hoch | hoch |
| Definitorische Schärfe nötig | D1, D2 (graduell operationalisieren) | D1, D4 (Grenze zu RPA/IPA) | D1, D5 (Grenze zu GenAI/Copilot) |
| Vergleichbarkeit der Fälle | hoch (gemeinsames Raster) | hoch (ein Bereich) | mittel (wenige Fälle) |
| Überschneidungsrisiko | Nr. 8, Nr. 11 gering bis mittel | Nr. 3 hoch | Nr. 5 mittel bis hoch |
| Abstraktionsrisiko | hoch | gering | mittel |
| Übertragungsrisiko (Prüfung, GenAI, KI allgemein) | mittel | hoch | hoch |
| Eignung für eigene Synthese (B Ziff. 3, Folie 90) | hoch | mittel | mittel |
| Seminarnähe (Folie 10, 15) | gut | gut | sehr gut (Controlling-Fokus) |
| Passung zu 8–10 Seiten | gut | gut | mittel, bedingt |

---

## 4. Empfehlung (keine Entscheidung)
**Option A**, mit einer Use-Case-Auswahl, die am WISO/EBSCO-Ergebnis geprüft wird. Gründe:
1. A bedient den Kern des agentenspezifischen Mehrwerts: Planung, Werkzeugnutzung, Ausführung und die daraus folgende Delegationsfrage (finance-ai-expert, Abschnitt 4). Keines der Nachbarthemen deckt das ab.
2. A verbindet die beiden Teile von Thema 9 strukturell: Aus der Autonomiestufe eines Use Case folgt die nötige Basis. Das passt zum Themenwortlaut „Schaffung der Basis“, der eher Voraussetzungen meint als gemessene Erfolgsfaktoren. Das ist meine Interpretation und nicht mit dem Dozenten geklärt.
3. A hat heute die breiteste Stufe-1-Basis und hält einer dünnen Domänenevidenz am besten stand, weil Lücken als Befund sichtbar werden.
4. A unterstützt Bewertungskriterium 3 („Eigene Erkenntnisse“) und vermeidet eine bloße Aneinanderreihung (Folie 90).

**Gegenargumente zu A:**
- Abstraktion.
- Übertragung nicht finanzspezifischer Raster.
- Der Professor erwartet möglicherweise mehr Praxisumsetzung (Folie 10). Gegenmittel: Praxisbeispiele aus Stufe 2.

**Brücke zwischen den beiden Agentenempfehlungen:** In A dürfen die Use Cases schwerpunktmäßig aus dem Rechnungswesen kommen, weil dort Prototypen existieren. Das nähert A der Empfehlung des source-researcher an.

**Weitere Optionen:**
- **B** als Alternative, wenn WISO/EBSCO weitere agentenspezifische Beiträge aus dem Rechnungswesen und Quellen zu IKS/GoBD liefert.
- **C** nur bei klar positivem Stufe-2-Befund.

**Zeitpunkt:** Die Entscheidung sollte erst nach einem ersten WISO/EBSCO-Durchgang fallen, aber vor dem Exposé (Folie 8: ca. 1 Woche bis zur Exposé-Ausarbeitung). Das Exposé (Folie 54) braucht die Forschungsfrage, eine dezimale Gliederung und ein vorläufiges Literaturverzeichnis. Beides verfasst der Student selbst; ins Literaturverzeichnis gehören nur geprüfte Quellen.

---

## 5. Empfohlenes Review-Design
**Bezeichnung: „strukturierte Literaturrecherche“.**

**Begründung:**
- Eine Person screent, es gibt keinen Zweitscreener.
- Der Umfang beträgt nur 8–10 Seiten.
- Stufe 2 wird einbezogen.
- Grundlagenwerke kommen per Known-Item- und Schneeballsuche hinzu.
- Das Feld ist jung und verändert sich schnell.

**Warum nicht „systematischer Review“:** Das würde eine vollständige, reproduzierbare Suche in mehreren Datenbanken, eine Qualitätsbewertung und ein Flussdiagramm verlangen. Bei diesem Umfang wäre das unverhältnismäßig, und das Label würde mehr behaupten, als geleistet wird.

**Warum nicht „Scoping Review“:** Inhaltlich passt er, weil ein junges Feld kartiert wird. Das Label setzt aber Standardelemente voraus (Protokoll, Charting, Berichtsstandard wie PRISMA-ScR). Ich rate davon ab, außer der Student will diesen Aufwand vollständig tragen.

**Wichtig:** Die WebSearch-Sondierung der KI-Agenten ist **Vorrecherche**, keine Datenbanksuche. Im Methodikteil darf sie nicht als Teil einer systematischen Suche erscheinen. Der KI-Einsatz ist offenzulegen (K1).

**Transparenzelemente im Methodikteil (Stichworte, kein Text):**
- Datenbanken und Zugangsweg, Suchstrings, Zeitraum, Sprachen, Stichtag
- Kriterien inkl. Quellen-Gate, Screening-Schritte
- **echte** Anzahl einbezogener Quellen je Stufe
- Grenzen

Details können in den Anhang. Der Anhang zählt nicht zum Seitenumfang (V S. 3–4), es muss aber im Text auf ihn verwiesen werden (V S. 8).

**Methodenquelle nötig:** Hinweise, NICHT_VERIFIZIERT und weder in der CSV noch hier geprüft – bitte durch source-researcher und citation-auditor prüfen lassen:
- Webster/Watson 2002 (MIS Quarterly, Konzeptmatrix)
- vom Brocke u. a. 2009 (ECIS) bzw. 2015 (CAIS), zur Dokumentation der Literatursuche
- Theisen als Quelle der Folie 64, aktuelle Auflage (Folie 68)

---

## 6. Minimal reproduzierbares Suchprotokoll (Vorschlag für Phase 2, passend zu `02_search/search_protocol.md`)
- **Termfamilien:** wie Protokoll Abschnitt 3.
  - Für A zusätzlich: „human-in-the-loop“, „human oversight“, „levels of automation“, delegation, Freigabe*.
  - Für B zusätzlich: GoBD, „internes Kontrollsystem“, „audit trail“, Prüfpfad.
  - Für C zusätzlich: Berichtswesen, Abweichungsanalyse, Kommentierung, FP&A.
- **Datenbanken** (Zugang jeweils offen, nur der Student kann sie abfragen): WISO, EBSCO Business Source (Filter Peer Reviewed), EconBiz. Optional Springer Professional und AIS eLibrary. Für B NWB und beck-online. Die Suchstrings aus dem source-researcher-Bericht, Abschnitt 8, sind als Startpunkt geeignet.
- **Getrennte Suchwege:**
  - Stufe 1: WISO mit Dokumenttyp wissenschaftliche Zeitschriften, Bücher, Dissertationen; EBSCO mit Filter Peer Reviewed.
  - Stufe 2: WISO, eingeschränkt über das Quellenfeld auf die Titel aus Anhang 4.
  - Beide getrennt protokollieren. Die Trefferbasis ist `DATENBANK_GESAMT`, nur mit echten Zahlen.
- **Zeitraum:** Vorschlag 2023–2026 für die agentenspezifische Datenbanksuche, also die LLM-Agenten-Phase.
  - **Ausnahmeregel nötig:** Q050 (1995), Q051 (2000), Q058 (2007), Q056 und Q060 (2020), Q006 und Q059 (2021) liegen außerhalb dieses Fensters.
  - Sie kommen über eine dokumentierte gezielte Grundlagenrecherche bzw. per Schneeball (`found_via`) hinein. Sonst entsteht ein Widerspruch zu E9.
- **Sprachen:** DE und EN.
- **Ausschlusscodes E1–E9:** präzisieren und freigeben lassen.
  - E1: Regel für externe Prüfung und interne Revision festlegen. Vorschlag: Ausschluss **oder** Aufnahme als gekennzeichnete Übertragungsevidenz (siehe Entscheidung 7).
  - E3: über den Merkmalskatalog nach D1 operationalisieren. Beispiel für Mindestmerkmale: Zielorientierung plus mehrstufige Planung plus Werkzeugnutzung bzw. Handeln. Copilot und GenAI nur zur Abgrenzung (`theme = TECHNIK_EINORDNUNG`).
- **Screening:** Titel und Abstract, dann Volltext. Jeder Ausschluss mit Code. Ein einzelner Screener ist eine Limitation. KI-gestütztes Vorscreening ist offenzulegen.
- **Dubletten:** über DOI, sonst normalisierter Titel plus Jahr (bereits im Protokoll).
- **Extraktion:** `theme`, `evidence_type`, `finance_area` gemäß Datenmodell.
  - Optional weitere Merkmale: Agententyp (D3), Autonomiestufe (nur A), Kontext CFO-intern oder Übertragung.
  - Als neue Spalten wäre das eine Änderung am Datenmodell und damit freigabepflichtig. Alternative: in `notes` erfassen.
- **Synthese:** thematisch über eine Konzeptmatrix. Belegtypen trennen: reale Anwendung, Prototyp, konzeptionell, Übertragung. Agentenbefunde nie aus RPA-, GenAI- oder allgemeinen KI-Befunden ableiten.
- **Stichtag:** Den Suchstichtag festhalten. Vor der Abgabe optional einen Aktualisierungslauf machen, denn die JETA-Sonderrubrik ist angekündigt.

---

## 7. Risiken und Limitationen

| Risiko | Folge für die Aussagekraft | Umgang (Stichworte) |
|---|---|---|
| Dünne agentenspezifische Stufe-1-Evidenz | keine verallgemeinernden Aussagen zu Verbreitung und Wirkung; Use Cases überwiegend prototypisch oder konzeptionell belegt | Evidenzgrad je Aussage ausweisen; Thesen als widerlegbare Behauptungen formulieren (Folie 81) |
| Verbreitung (Folie 10) nicht wissenschaftlich belegt | dieser Teil der Aufgabe bleibt in allen Optionen schwach | als Lücke benennen; Stufe 2 nur zur Illustration |
| Effizienz und Effektivität: nur Q001 als Einzelexperiment (Inhalt ungeprüft) | kein Wirkungsnachweis | Einzelfall kennzeichnen; die Zahlen aus der Suchmaschinen-Zusammenfassung nicht verwenden |
| Unscharfer Agentenbegriff | uneinheitliche Ein- und Ausschlüsse nach E3; Vermischung mit RPA oder GenAI | Merkmalskatalog nach D1 vorab festlegen; Grenzfälle offenlegen |
| Übertragung (Prüfung bzw. GenAI bzw. RPA bzw. KI allgemein → CFO-Agenten) | eingeschränkte Gültigkeit | jede Übertragung kennzeichnen; Q059 als Gegenposition |
| Kein Zugang zu WISO/EBSCO | Suche weniger reproduzierbar, eher Known-Item-lastig | auf EconBiz, Verlagsportale und Schneeball ausweichen und das offen als Grenze benennen |
| Volltextlücken (alles NUR_METADATA, Peer Review überall UNKLAR) | keine Seitenbelege, keine Aufnahme in die Evidenzmatrix | zuerst Open-Access-Texte lesen (laut Snippets Q001, Q007, Q010, Q012; Q050 als HTML); Fernleihe ist zumutbar (Folie 72), dafür Zeitpuffer einplanen |
| Begutachtung fraglich (MDPI, IEEE Access, Inderscience, BISE-Catchword, BPM-Forum) | Stufe-1-Status unsicher | Prüfung durch den citation-auditor |
| Verzerrung in Stufe 2 (Autoren aus Beratung oder bei Anbietern) | Interessenkonflikte | CRAAP-Prüfung; nie alleiniger Beleg |
| Dynamisches Feld | Ergebnis kann bei Abgabe veraltet sein | Stichtag festhalten; optionaler Aktualisierungslauf |

---

## 8. Widersprüche zwischen den beiden Agentenberichten (offengelegt, nicht geglättet)
1. **Controlling:**
   - source-researcher: „0 Stufe-1-Kandidaten“.
   - finance-ai-expert: Q059 (Controlling, Stufe-1-Kandidat, konzeptionell).
   - Lesart: Es gibt 1 konzeptionellen Kandidaten, aber 0 agentenspezifische.
2. **Treasury:**
   - source-researcher: „0“.
   - finance-ai-expert: Q060 (konzeptionell, nicht agentenspezifisch).
   - Das ändert nichts am Urteil, dass Treasury nicht empfehlenswert ist.
3. **Einordnung von Q001 Resende:**
   - source-researcher und CSV: ACCOUNTING.
   - finance-ai-expert: „Controlling / Accounting“.
   - Entscheidend für Option C. Am Volltext klären (Open Access laut Snippet).
4. **Prototypen aus der Prüfung (Q002):**
   - source-researcher: „E1 prüfen“, also möglicher Ausschluss.
   - finance-ai-expert: als „Übertragung kennzeichnen“, also Aufnahme.
   - Das ist eine methodische Grundsatzentscheidung (Entscheidung 7). Sie entscheidet über die Tragfähigkeit von B.
5. **Q054 (BISE-Catchword):**
   - source-researcher: „Titel nicht auffindbar, DOI-Zuordnung unbestätigt“.
   - finance-ai-expert: als Kandidat geführt.
   - Inzwischen per Crossref VERIFIZIERT (68(5), 1191–1204). Offen bleibt, ob das Catchword-Format begutachtet wird.
6. **Empfehlungen:**
   - source-researcher: Use Cases aus dem Rechnungswesen plus konzeptionelle Erfolgsfaktoren (nahe B mit Elementen von A).
   - finance-ai-expert: nennt Z1 als „tragfähigste Literatur“ zuerst und bewertet Z1, Z2 und Z4 jeweils als „gut“.
   - Unterschiedliche Gewichtung, keine harte Gegensätzlichkeit.
7. **Jahresangaben:** Beide Berichte enthalten von Crossref abweichende Jahre:
   - Q002: 2025 → 2026
   - Q011: 2025 → 2026
   - Q060: 2019 → 2020
   - Q008 bleibt WIDERSPRUECHLICH (2022 gegenüber Heft 2024; auch die Autorenreihenfolge weicht ab).
8. **Inhaltsbehauptung zu Q001:** „150 experimentelle Fälle, größter Effizienzgewinn beim Agenten“ steht nur bei finance-ai-expert. Die Angabe stammt aus einer Suchmaschinen-Zusammenfassung und ist für die Optionsbewertung nicht verwendbar.
9. **Sapkota (Q011):** source-researcher führt die Quelle als Kandidat, finance-ai-expert nur als Hinweis. Inzwischen per Crossref VERIFIZIERT (Information Fusion 126, 103599). Die D1-Referenz „Hinweis Sapkota“ meint also Q011.

---

## 9. Entscheidungen mit Freigabebedarf (nummeriert)

**Vor der Festlegung des Zuschnitts bzw. vor dem Exposé:**
1. Zuschnitt: A, B, C oder Verschiebung bis nach dem WISO/EBSCO-Durchgang.
2. Teilbereich(e): nur Controlling, nur Rechnungswesen oder beide. Treasury ausschließen oder höchstens als gekennzeichnetes Randbeispiel.
3. **D1 Definitionsansatz:** Etikett oder Merkmalskatalog. Bei Merkmalskatalog: welche Mindestmerkmale?
4. **D2 Agentur:** binär oder graduell. Bei A zwingend graduell und dann mit Stufenkriterien.
5. **D3 Umfang:** einzelner werkzeugnutzender LLM-Agent, agentische KI bzw. Multi-Agenten-System, klassische Multi-Agenten-Systeme nur als Begriffsgeschichte?
6. Verwandte Begriffsentscheidungen aus dem finance-ai-expert-Bericht:
   - D4: Ist eine IPA-Strecke mit LLM-Baustein schon ein Agent?
   - D5: Copilot nur zur Abgrenzung oder als Vorstufe mitbehandeln?
   - D8: deutsche Terminologie.
7. Umgang mit Evidenz aus der Prüfung (Q002, Q003, Q058; interne Revision Q004): Ausschluss nach E1 oder Aufnahme als gekennzeichnete Übertragungsevidenz.
8. Gehört die interne Revision zur CFO-Funktion (D7)? Kandidat für die „offenen Punkte“ im Exposé bzw. für den Präsenztermin (Folie 7).
9. Primärer Fragetyp nach Folie 64. Die Forschungsfrage formuliert der Student selbst.

**Phase 2 (Methodik):**

10. Bezeichnung des Review-Typs. Empfehlung: „strukturierte Literaturrecherche“.
11. Datenbanken, nach Prüfung des Zugangs: WISO, EBSCO, EconBiz; optional Springer Professional und AIS eLibrary; für B NWB und beck-online.
12. Zeitraum (Vorschlag 2023–2026) und Ausnahmeregel für Grundlagenliteratur außerhalb des Fensters.
13. Sprachen DE/EN.
14. Freigabe der Ausschlusscodes E1–E9 einschließlich der Präzisierung von E1 und E3.
15. Q014 (Praxisfachbuch Bliefert): Laut Datenmodell gibt es AUFGENOMMEN_ERGAENZEND nur für PRAXISBEITRAG. Q014 kann also nur als Stufe 1 aufgenommen oder ausgeschlossen werden – oder das Datenmodell wird geändert (freigabepflichtig).
16. Fachzeitschriften außerhalb von Anhang 4 (z. B. Journal of Accountancy): Standard ist kein Einbezug, möglich nur per Einzelfreigabe.
17. Zusätzliche Extraktionsmerkmale (Agententyp, Autonomiestufe, Übertragung): als neue Spalten (Änderung am Datenmodell) oder in `notes`.
18. Suchstichtag und optionaler Aktualisierungslauf vor der Abgabe.
19. KI-gestütztes Screening: Ob und wie es zulässig ist, ist wegen K1 offen. Für den Präsenztermin bzw. die offenen Punkte im Exposé vormerken.

---

## 10. Übergabe an den Orchestrator
- Bitte die Optionen A–C vom `finance-ai-expert` fachlich gegenprüfen lassen. Schwerpunkte:
  - Operationalisierung der Autonomiestufen in A
  - Abgrenzung von B zu Nr. 3
  - Einordnung von Q001
- Bei der Übernahme nach `01_scope/topic_options.md` die alten IDs Q052/Q053/Q055/Q061/Q062 auf Q006/Q009/Q012/Q002/Q001 umstellen.
- Erst nach Freigabe durch den Studenten `00_admin/decision_log.md`, `01_scope/` und `02_search/search_protocol.md` aktualisieren.
- Nächste Aufgaben für den Studenten selbst (Vorschlag):
  - erster WISO/EBSCO-Durchgang mit den Strings aus dem source-researcher-Bericht, Abschnitt 8, einschließlich Protokollierung
  - Volltext von Q001 lesen (Open Access laut Snippet), um Agentenbegriff und Einordnung zu prüfen
  - Zugang zu Q006, Q051, Q057 und Q059 klären

Gelesene Dateien (nicht verändert):
- /home/user/reyan232/CLAUDE.md
- /home/user/reyan232/00_admin/seminar_requirements.md
- /home/user/reyan232/00_admin/decision_log.md
- /home/user/reyan232/00_admin/datenmodell.md (nur Vokabular)
- /home/user/reyan232/01_scope/topic_options.md
- /home/user/reyan232/02_search/search_protocol.md
- /home/user/reyan232/03_sources/literature.csv
- /home/user/reyan232/05_research_notes/2026-11-07_phase1_sondierung_source-researcher.md
- /home/user/reyan232/05_research_notes/2026-11-07_phase1_begriffe_evidenz_finance-ai-expert.md