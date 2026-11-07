# Wissenschaftliche Recherche | PROTOKOLL-ENTWURF, noch keine durchgeführte Suche

> Herkunft: gemischt – Starterpaket v3 + Strukturierung (Claude Code, 2026-11-07). **Status: ENTWURF – nicht freigegeben.** Abschnitte mit „VORSCHLAG“ werden erst nach ausdrücklicher Freigabe des Studenten verbindlich (`00_admin/decision_log.md`).

## 1. Rahmen
- Seminarscope: KI-Agenten/Agentic AI in der Unternehmens-CFO-Funktion (**Realwirtschaft**); konkrete Use Cases und betriebliche Erfolgsfaktoren. Nicht primär Bankwesen/Finanzdienstleistungsindustrie.
- Forschungsfrage und Eingrenzung: **noch nicht freigegeben** (`01_scope/research_question.md`).
- Design: nach methodischer Angemessenheit wählen. „Systematische Literaturrecherche/Review“ nur bei real dokumentierter, reproduzierbarer Suche in mehreren einschlägigen Datenbanken mit vorab definierten Kriterien; sonst korrekt „strukturierte Literaturrecherche“. Keine PRISMA-Zahlen ohne tatsächliche Durchführung.

## 2. Datenbanken – VORSCHLAG, Zugang über die Hochschulbibliothek erst prüfen
Kein Zugang wird hier als gegeben behauptet. Lizenzierte Datenbanken kann nur der Student mit Hochschulzugang durchsuchen; KI-Agenten können sie nicht abfragen und dürfen keine Trefferzahlen daraus angeben.

| Kandidat | Zweck | Zugang geprüft? |
|---|---|---|
| **Vom Professor genannt (V S. 18):** WISO, EBSCO, Springer, NWB, ECONBIZ, beck-online; Elektronische Zeitschriftenbibliothek (EZB) | Controlling/Finanzen, deutschsprachige Fach- und Praxisliteratur | über Hochschulbibliothek prüfen (Login mit Hochschulaccount) |
| EconBiz (Suchportal der ZBW) | wirtschaftswissenschaftliche Literatur, frei durchsuchbar | Portal frei erreichbar; Volltextzugang je Titel prüfen |
| Zeitschriften aus V Anhang 4 (S. 25) | Controlling/Finanzen; viele davon Praxis-Fachzeitschriften | Zulassung als Evidenz hängt von Entscheidung K2 ab |
| Scopus oder Web of Science (falls lizenziert) | interdisziplinäre Abdeckung, Zitationsverfolgung | offen |
| AIS eLibrary (Informationssysteme-Konferenzen und -Journals) | agentische KI in Unternehmen, Design-Science-Studien | offen |
| IEEE Xplore / ACM Digital Library | Agenten-Technik (Tool-Use, Multi-Agenten-Systeme) | offen |
| Verlagsportale (z. B. SpringerLink, ScienceDirect) | Fachbücher, Sammelbände, Journals | offen |
| Google Scholar, Crossref, OpenAlex, Hochschulkatalog | **nur Finder/Metadaten**, keine Forschungsevidenz | frei |

## 3. Suchterm-Familien – zur Prüfung, nicht als gelaufene Suchen ausgeben
- **Technologie:** `agentic AI`, `AI agent*`, `autonomous agent*`, `LLM-based agent*`, `multi-agent system*`, `KI-Agent*`
- **Finanzfunktion:** `finance function`, `CFO`, `corporate finance`, `management accounting`, `controlling`, `financial accounting`, `accounting`, `treasury`, `Rechnungswesen`
- **Erkenntnisinteresse:** `use case*`, `application*`, `adoption`, `implementation`, `success factor*`, `critical success factor*`, `governance`, `readiness`, `Erfolgsfaktor*`
- Abgrenzungsbegriffe nur zum Ausschluss/Vergleich: `robotic process automation`, `chatbot`, `generative AI` (keine Gleichsetzung mit Agenten).

## 4. Ein-/Ausschlusskriterien – VORSCHLAG
- **Hinweise des Professors (V S. 18–19):** themenspezifische Literatur statt Standardlehrbücher; Zeitschriftenartikel für Aktualität und Praxisbezug; aktuelle Dissertationen als Fundus; Internetquellen nur, wenn keine Druckfassung existiert; Wikipedia unzulässig (L S. 7).
- **Inklusion (Quellen-Gate):** peer-reviewte Zeitschriftenartikel und Konferenzbeiträge, wissenschaftliche Fachbücher/Sammelbandbeiträge mit eindeutigem Verlag und Autorenschaft, überprüfbare Dissertationen. Publikationsstatus und Volltextzugang getrennt bewerten.
- **Exklusion als Forschungsbeleg:** YouTube/Video, Blogs, Anbieterwebsites/Marketing, Beratungs-Whitepaper, Presse, Wikipedia, Social Media, Preprints, unbegutachtete Working Papers, KI-generierte Antworten. Seminarfolien sind **verbindliche Aufgabenquelle**, aber keine Forschungsevidenz.
- **Ausschlusscodes (ENTWURF):** `E1` kein Bezug zur Finanzfunktion realwirtschaftlicher Unternehmen · `E2` Finanzindustrie/Banken als Untersuchungsgegenstand · `E3` kein Agentenbezug (nur RPA/klassisches ML/Chatbot, ohne agentische Merkmale) · `E4` unzulässiger Publikationstyp · `E5` Metadaten nicht verifizierbar · `E6` Dublette · `E7` Volltext nicht beschaffbar (auch nicht per Fernleihe) · `E8` Sprache außerhalb DE/EN · `E9` außerhalb des freigegebenen Zeitraums.
- Zeitraum, Sprachen und Publikationstypen: **offen** (Freigabe).

## 5. Ablauf und Dokumentation
1. Jeder tatsächlich durchgeführte Lauf → `02_search/search_log.csv` (Datum, ausführende Person/Agent, Datenbank, Interface, **exakter** Suchstring, Filter, Trefferzahl + Zählbasis, Exportdatei).
2. Rohexporte lokal unter `02_search/exports/` (nicht in Git).
3. Dubletten: DOI, sonst normalisierter Titel + Jahr (Validator meldet Verdachtsfälle).
4. Screening in `02_search/screening_log.csv`: Titel/Abstract → Volltext; jeder Ausschluss mit Code und Begründung.
5. Kandidaten und Aufnahmeentscheidung in `03_sources/literature.csv`; nur `AUFGENOMMEN` darf in `03_sources/evidence_matrix.csv`.
6. Schneeballsuche (Rückwärts/Vorwärts) mit `found_via = SCHNEEBALL:<source_id>` kennzeichnen.
7. Nach jedem Arbeitsgang `python3 scripts/validate_research_data.py`.

## 6. Synthese
- Evidenz nach `theme` (Use Case, Erfolgsfaktor, Nutzen Effizienz/Effektivität, Risiko/Grenze, Umsetzung, Verbreitung) und `finance_area` ordnen; konkurrierende Befunde in `related_evidence` sichtbar machen.
- Trenne wissenschaftlich belegte reale Anwendungen, konzeptionelle Vorschläge und unbelegte Anbieterbehauptungen. Begrenzte Evidenzlage ehrlich benennen; allgemeine RPA-/GenAI-Befunde nicht als Agentenbefunde umdeuten.

## 7. Grenzen der Suche (laufend ergänzen)
- Noch keine Suchläufe durchgeführt; keine Trefferzahlen vorhanden – keine erfinden.
