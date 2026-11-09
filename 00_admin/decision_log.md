# Entscheidungen und Freigaben

> Herkunft: gemischt – Einträge des Orchestrators (Claude Code) und des Studenten. Nur Einträge mit „Freigegeben: Ja“ sind verbindlich.

Freigabepflichtig (vorab, ausdrücklich): Thema/Eingrenzung, Forschungsfrage, Gliederung, Methodik/Review-Typ, Ein-/Ausschlusskriterien, Zitierstil, Änderungen an studentischem Text, externe Accounts/Käufe/kostenpflichtige Dienste, wesentliche Änderungen an `CLAUDE.md`, Agenten oder Skills.

| Datum | Gegenstand | Status | Freigegeben vom Studenten? | Grundlage |
|---|---|---|---|---|
| 2026-11-07 | Zuordnung Thema 9 aus Themenliste | BESTÄTIGT – Zuteilung über Moodle laut Studenten erfolgt | Ja (Rückfrage im Chat) | Themenliste WS 2026/27 S. 1 |
| 2026-11-07 | Seminar-PDFs und Quellenregeln berücksichtigen | REGELN TEILWEISE GEPRUEFT, Sonderrichtlinien fehlen | Dokumente bereitgestellt, Anwendung in Projekt übernommen | Seminarfolien S. 10, 14, 54–90 |
| 2026-11-07 | Starterpaket v3 in Repo-Branch `claude/finance-ai-agents-research-system-llfffr` übernommen (Commit 1 unverändert, Commit 2 Ergänzungen) | UMGESETZT | Auftrag durch Bootstrap-Prompt | Bootstrap-Prompt Abschn. 9 |
| 2026-11-07 | Phase-0-Abgleich PDFs ↔ Anforderungsmatrix; Ergänzungen/Korrekturen, Konfliktpunkte K1–K4 | UMGESETZT, vom Studenten gegenzuprüfen | Nein (Prüfung, keine Entscheidung) | `00_admin/seminar_requirements.md` |
| 2026-11-07 | Datenschutz: PDFs, Entwurf, Feedback-/QS-Berichte, Exporte, reales KI-Protokoll nicht in Git (öffentliches Repo) | TECHNISCHE VORKEHRUNG | Ausstehend – Student kann lockern/verschärfen | `.gitignore`, `00_admin/compliance_status.md` |
| 2026-11-07 | Schreibschutz für `06_student_draft/` per `.claude/settings.json` (permissions.deny) | TECHNISCHE VORKEHRUNG | Ausstehend | Human-Author-Regel, Prompt Abschn. 8 |
| 2026-11-07 | CSV-Vokabular auf deutsche Statuswerte vereinheitlicht (`NUR_METADATA`, `NUR_ABSTRACT`, `VOLLTEXT_GELESEN`, `NICHT_VERIFIZIERT` …) | UMGESETZT (Dateien waren leer) | Ausstehend | `00_admin/datenmodell.md` |
| 2026-11-07 | Neue Cloud-Umgebung „reyan232 – Seminar-Recherche“ mit Netzwerkzugriff auf www.haw-landshut.de und www.econbiz.de; Sitzung darauf umgestellt | UMGESETZT | Ja (Freigabedialog der Umgebung bestätigt) | Abruf Fakultätsleitfaden/Satzung war vom Netzwerk blockiert |
| 2026-11-07 | Abgleich 2: Professorenvorgaben 10/2017, Bewertungsformular 2024, Fakultätsleitfaden 04/2024, HAW-Satzung GWP 2022 ausgewertet; Rangfolge dokumentiert; K5–K9 per Rangregel aufgelöst | UMGESETZT, vom Studenten gegenzuprüfen | Nein (Prüfung, keine Entscheidung) | `00_admin/seminar_requirements.md` Abgleich 2 |
| 2026-11-07 | Compliance-Status bleibt TEILWEISE_GEPRUEFT (KI-Regeln für die schriftliche Arbeit, Termine, Themenzuteilung offen) | UMGESETZT | – | `00_admin/compliance_status.md` |
| 2026-11-07 | Offizielle Bewertungskriterien in `04_quality/quality_rubric.md` übernommen (ohne Gewichtung) | UMGESETZT (Dokumentation) | – | Bewertungsformular 2024-01-02 |
| 2026-11-07 | Zitierstil: Fußnoten-Kurzbeleg + Literaturverzeichnis nach Professorenvorgaben (K3) in `CLAUDE.md`, Skills und Agenten übernommen | UMGESETZT | Ja (Rückfrage im Chat) | V S. 10–16 |
| 2026-11-07 | Quellen-Gate (K2): **Option B – zweistufig** (Stufe 1 Forschungsevidenz; Stufe 2 Praxis-Fachzeitschriften laut V Anhang 4 mit CRAAP-Prüfung, nur ergänzend); umgesetzt in `CLAUDE.md`, Skills, Agenten, Datenmodell, Validator (`AUFGENOMMEN_ERGAENZEND`) und Tests | UMGESETZT | Ja (Rückfrage im Chat) | V S. 19, 25–29; B Ziff. 4 |
| 2026-11-07 | Phase 1 gestartet (Themenfokussierung: Sondierung durch source-researcher und finance-ai-expert, danach Optionen durch methodology-advisor) | IN ARBEIT | Ja („Ja“ im Chat) | CLAUDE.md Phasen |
| 2026-11-07 | Phase 1: Optionen A (Autonomie-/Delegationsrahmen, Controlling + Rechnungswesen), B (Rechnungswesen), C (Controlling) vorgelegt; Empfehlung A nach eigener WISO/EBSCO-Prüfung | VORGELEGT – Entscheidung des Studenten ausstehend | Nein | `01_scope/topic_options.md` |
| 2026-11-07 | Umgebung „reyan232 – Seminar-Recherche“ um api.crossref.org, api.openalex.org, doi.org erweitert (DOI-/Metadatenprüfung) | UMGESETZT | Ja (Freigabedialog bestätigt) | Abruf war vom Netzwerk blockiert |
| 2026-11-09 | Umgebung um www.mdpi.com und mdpi-res.com erweitert (Open-Access-Volltext Q001, CC BY 4.0); Verlag blockt automatische Downloads (403) – kein Umgehungsversuch, Student lädt selbst | UMGESETZT | Ja (Freigabedialog bestätigt) | Anfrage des Studenten |
| | Endgültige Forschungsfrage | OFFEN | Nein | |
| | Eingegrenzter Finance-Teilbereich (Controlling / Accounting / Treasury) | OFFEN | Nein | |
| | Review-Typ / konkrete Methodik / Ausschlusscodes | OFFEN | Nein | `02_search/search_protocol.md` (Entwurf) |
