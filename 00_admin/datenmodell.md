# Datenmodell der Recherche-Dateien (verbindliches Vokabular)

> Herkunft: KI-generiert (Claude Code, Setup 2026-11-07) – technische Projektdokumentation, nicht zur Abgabe.

Alle CSV-Dateien sind UTF-8, Komma-getrennt, erste Zeile = Kopfzeile. Spalten­reihenfolge nicht ändern; neue Spalten nur nach Freigabe und zusammen mit `scripts/validate_research_data.py` anpassen. Leere Zelle = „noch nicht erhoben“, **nie** „geschätzt“. Datumsangaben immer `JJJJ-MM-TT`. Mehrfachwerte mit `;` trennen.

Der Validator (`python3 scripts/validate_research_data.py`) prüft Struktur und Konsistenz, **nicht** die fachliche Richtigkeit.

## 03_sources/literature.csv – Quellenregister (alle Kandidaten, auch ausgeschlossene)

| Spalte | Bedeutung / zulässige Werte |
|---|---|
| `source_id` | eindeutige ID, Schema `Q001`, `Q002`, … (wird auch als BibTeX-Key verwendet) |
| `title`, `authors`, `year` | vollständiger Titel; Autor(en) `Nachname, Vorname; Nachname, Vorname`; Jahr vierstellig |
| `source_type` | **Stufe 1 – Forschungsevidenz:** `ZEITSCHRIFTENARTIKEL`, `KONFERENZBEITRAG`, `FACHBUCH`, `SAMMELBANDBEITRAG`, `DISSERTATION` · **Stufe 2 – ergänzend:** `PRAXISBEITRAG` (Praxis-Fachzeitschrift, vorrangig laut Anhang 4 der Professorenvorgaben) · **nur zur Ausschluss-Dokumentation:** `PREPRINT`, `WORKING_PAPER`, `GRAUE_LITERATUR`, `SONSTIGES` |
| `publication` | Journal / Tagungsband / Buchtitel / Hochschule (bei Dissertation) |
| `publisher` | Verlag bzw. veranstaltende Organisation |
| `volume_issue_pages` | z. B. `45(3), 101–120` – nur aus geprüften Metadaten |
| `doi`, `isbn`, `urn`, `publication_url` | Kennungen; DOI ohne `https://doi.org/`-Präfix möglich; ISBN wird auf Prüfziffer getestet |
| `peer_review_status` | `BESTAETIGT`, `NICHT_BESTAETIGT`, `NICHT_ZUTREFFEND` (Buch/Dissertation), `UNKLAR` |
| `peer_review_evidence` | Nachweis, z. B. URL der Journal-/Tagungsrichtlinie zum Begutachtungsverfahren |
| `metadata_status` | `VERIFIZIERT`, `NICHT_VERIFIZIERT`, `WIDERSPRUECHLICH` |
| `metadata_evidence` | mind. ein zuverlässiger Metadatennachweis (Verlagsseite, Crossref, Hochschulkatalog …) |
| `access_level` | `KEIN_ZUGRIFF`, `NUR_METADATA`, `NUR_ABSTRACT`, `VOLLTEXT_GELESEN` |
| `integrity_flags` | leer = nicht geprüft; `KEINE_BEKANNT`, `ZURUECKGEZOGEN`, `KORRIGIERT`, `KONTROVERS` |
| `finance_area` | `CONTROLLING`, `ACCOUNTING`, `TREASURY`, `FINANZFUNKTION_UEBERGREIFEND`, `TECHNIK_GRUNDLAGEN`, `NICHT_ZIELBEREICH` (z. B. Banken) |
| `found_via` | Rückverfolgung: `search_id` aus `search_log.csv` oder `SCHNEEBALL:<source_id>`, `HINWEIS_DOZENT`, `STUDENT`, `SEMINARFOLIE` |
| `decision` | `KANDIDAT`, `AUFGENOMMEN` (Stufe 1), `AUFGENOMMEN_ERGAENZEND` (Stufe 2, nur `PRAXISBEITRAG`), `AUSGESCHLOSSEN`, `ZURUECKGESTELLT` |
| `decision_reason` | Pflicht bei `AUSGESCHLOSSEN`/`ZURUECKGESTELLT`/`AUFGENOMMEN_ERGAENZEND` (dort inkl. CRAAP-Prüfung) |
| `added_by`, `added_date` | wer/wann erfasst (z. B. `source-researcher (KI)`, `Student`) |
| `notes` | freie Notiz |

**Zweistufiges Quellen-Gate** (Entscheidung des Studenten vom 2026-11-07, Konflikt K2 = Option B).

**Gate für `AUFGENOMMEN` (Stufe 1)** (vom Validator erzwungen): zulässiger `source_type`; Titel/Autor/Jahr/Publikation vorhanden; `metadata_status = VERIFIZIERT` mit `metadata_evidence`; bei Zeitschrift/Konferenz `peer_review_status = BESTAETIGT` mit `peer_review_evidence`; mind. eine Kennung (DOI/ISBN/URN/URL); nicht `ZURUECKGEZOGEN`; mindestens `NUR_ABSTRACT`; `found_via` gesetzt.

**Gate für `AUFGENOMMEN_ERGAENZEND` (Stufe 2)**: nur `source_type = PRAXISBEITRAG`; Titel/Autor (sonst „o. V.“)/Jahr/Publikation; `metadata_status = VERIFIZIERT` mit Nachweis; Kennung; nicht `ZURUECKGEZOGEN`; mindestens `NUR_ABSTRACT`; `found_via`; `decision_reason` mit CRAAP-Prüfung (Currency, Relevance, Authority, Audience, Purpose; Booklet ZBW S. 13). Zeitschrift nicht in Anhang 4 → Hinweis, Einzelfreigabe im `decision_log.md` nötig. In der Evidenzmatrix: `reliability` höchstens `MITTEL`, `limitations` Pflicht. Stufe-2-Quellen stützen Praxisbeispiele, Verbreitung und aktuelle Entwicklungen, **nie allein** verallgemeinernde oder empirische Wirkungsaussagen. Working Papers, Preprints, Whitepaper, Blogs, Wikipedia und KI-Ausgaben bleiben ausgeschlossen.

## 03_sources/evidence_matrix.csv – Befund ↔ Beleg

| Spalte | Bedeutung / zulässige Werte |
|---|---|
| `evidence_id` | eindeutig, Schema `E001` … |
| `source_id` | muss in `literature.csv` existieren **und** `AUFGENOMMEN` oder `AUFGENOMMEN_ERGAENZEND` sein |
| `claim_or_finding` | Befund/Konzept in eigenen Stichworten (keine Abgabeformulierung) |
| `theme` | `TECHNIK_EINORDNUNG`, `USE_CASE`, `VERBREITUNG`, `NUTZEN_EFFIZIENZ`, `NUTZEN_EFFEKTIVITAET`, `ERFOLGSFAKTOR`, `RISIKO_GRENZE`, `UMSETZUNG_PRAXIS`, `METHODIK`, `SONSTIGES` |
| `finance_area` | wie oben |
| `evidence_type` | `EMPIRISCH_QUANTITATIV`, `EMPIRISCH_QUALITATIV`, `FALLSTUDIE`, `EXPERIMENT_PROTOTYP`, `LITERATURREVIEW`, `KONZEPTIONELL`, `DEFINITION` |
| `source_location` | überprüfbare Fundstelle (Seite/Abschnitt/Tabelle) – Seitenangaben **nur** bei `VOLLTEXT_GELESEN` |
| `access_level` | wie oben; darf nicht höher sein als in `literature.csv`; `NUR_METADATA`/`KEIN_ZUGRIFF` unzulässig |
| `verified_against_text` | `JA` (nur mit `VOLLTEXT_GELESEN` + Fundstelle), `TEILWEISE`, `NEIN` |
| `reliability` | `HOCH`, `MITTEL`, `GERING`, `UNKLAR` |
| `limitations` | methodische Grenzen (Stichprobe, Kontext, Agentenbegriff unscharf …) |
| `related_evidence` | z. B. `stuetzt:E003; widerspricht:E007` – konkurrierende Befunde sichtbar machen |
| `recorded_by`, `recorded_date`, `notes` | Herkunft der Zeile |

## 02_search/search_log.csv – jeder tatsächlich durchgeführte Suchlauf

`search_id` (`S001` …), `search_date`, `executed_by`, `database`, `interface` (z. B. EBSCOhost, Verlagsportal, WebSearch-Tool), `search_string` (exakt, kopiert), `filters`, `result_count` (ganze Zahl oder leer), `result_count_basis` (`DATENBANK_GESAMT`, `ZURUECKGEGEBENE_TREFFER`, `UNBEKANNT`), `export_path`, `notes`.
Suchmaschinen-/Tool-Treffer sind **keine** Datenbank-Gesamttreffer → `ZURUECKGEGEBENE_TREFFER`.

## 02_search/screening_log.csv – Auswahlentscheidungen

`source_id`, `search_id`, `title`, `title_abstract_decision`, `full_text_decision` (je `EINGESCHLOSSEN`, `AUSGESCHLOSSEN`, `UNKLAR` oder leer), `exclusion_code` (Codes laut freigegebenem Suchprotokoll), `exclusion_reason` (Pflicht bei Ausschluss), `reviewer`, `screening_date`, `notes`.

## 04_quality/benchmark_register.csv – Qualitätsmaßstäbe (keine Fachevidenz)

`benchmark_id` (`B001` …), `benchmark_type` (`HOCHSCHULRUBRIK`, `SCHREIBLEITFADEN`, `ABSCHLUSSARBEIT`, `SEMINARARBEIT`, `PREISGEKROENTE_ARBEIT`, `SONSTIGES`), `title`, `degree_type`, `institution`, `year`, `grade` (nur mit Nachweis), `grade_verified` (`JA`, `NEIN`, `UNBEKANNT`), `grade_evidence_url`, `document_url`, `access_date`, `quality_criterion`, `notes`.

## 00_admin/ki_nutzungsprotokoll.csv – reales KI-Einsatzprotokoll (lokal, nicht in Git)

`datum`, `tool_agent`, `phase_aufgabe`, `verwendungszweck`, `art_der_ausgabe`, `vom_studenten_genutzt`, `originalquellen_geprueft`, `qualitaet_probleme`, `menschliche_entscheidung`, `offene_fragen`. Leere Vorlage: `00_admin/ki_nutzungsprotokoll.vorlage.csv`.

## Herkunftskennzeichnung von Notizen und Berichten

Jede Markdown-Datei (außer `README.md`) in `05_research_notes/`, `07_feedback/` und `04_quality/reports/` beginnt in den ersten 10 Zeilen mit einer Zeile
`> Herkunft: KI-generiert (<Agent/Skill>, <Datum>) – nicht zur Abgabe` oder `> Herkunft: Student` bzw. `> Herkunft: gemischt (…)`.
Der Validator meldet fehlende Kennzeichnungen als Fehler.

## 03_sources/library.bib

Nur Einträge, deren Key einer `source_id` mit `metadata_status = VERIFIZIERT` entspricht. Datei ist Zotero-kompatibel (BibTeX-Import; Zotero wird von der Hochschulbibliothek unterstützt, Seminarfolien Folie 75).
