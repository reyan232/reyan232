# Academic Research Assistant – Finance AI Agents | Version 3

**Auf aktuelle Seminarunterlagen WS 2026/27 von Prof. Dr. Patrick Dieses angepasst.** Bachelor-Studienarbeit: **8–10 Seiten Textteil einschließlich Abbildungen/Tabellen**; offizielles Thema Nr. 9 **„Einsatz von KI-Agenten in der Finanzfunktion: Use Cases und Erfolgsfaktoren“**. Untersuchungsrahmen: **CFO-Funktion realwirtschaftlicher Unternehmen**, nicht Banken/Finanzindustrie.

## Enthalten
- Orchestrator-Anweisungen in `CLAUDE.md`.
- Sechs echte Claude-Code-Subagents in `.claude/agents/`.
- **Sieben** Skills in `.claude/skills/`, einschließlich `seminar-deliverables` und `university-policy-check`.
- Wissenschaftliche Suchprotokolle, Quellenregister/Evidenzmatrix, Qualitätsrubrik, lokaler Validator und Tests.
- Die **beiden original hochgeladenen Seminar-PDFs** als private, nicht git-versionierte Regelgrundlage.
- **Seminar-Anforderungsmatrix mit Folienfundstellen** unter `00_admin/seminar_requirements.md` und `00_admin/requirements_checklist.md`.
- **KI-Nutzungsprotokoll** unter `00_admin/ki_nutzungsprotokoll.csv` für die verpflichtende Reflexion des KI-Einsatzes im Kolloquium.

## Schnellstart
1. ZIP entpacken, in den Projektordner wechseln und `claude` starten.
2. Schreibe: `Lies CLAUDE.md, 00_admin/seminar_requirements.md und 00_admin/compliance_status.md. Prüfe alle sechs Agents und sieben Skills. Beginne keine umfangreiche Suche, verfasse keinen abgabefertigen Text. Nenne mir die eine nächste Entscheidung.`
3. Die **zwei Original-Seminar-PDFs sind bereits enthalten** (`00_admin/hochschulregeln/`). Bitte Claude Code, zuerst die PDF-Originale mit der daraus abgeleiteten Anforderungsmatrix abzugleichen. Beziehe dich auf die aufgedruckten Foliennummern, nicht automatisch auf die PDF-Seitenzahlen.
4. Lade die **noch fehlenden** gesonderten Moodle-Dokumente (allgemeiner Fakultätsleitfaden, Vorgaben Prof. Dieses, Bewertungskriterien, KI-Regeln) in denselben privaten Ordner und führe `/university-policy-check` aus.
5. Bestätige, ob offizielles **Thema 9** tatsächlich dir zugeteilt wurde, und entscheide nach Beratung Forschungsfrage und Eingrenzung.

## Methodische Leitlinien
Nur wissenschaftliche Fachliteratur als inhaltliche Evidenz. Blogs, YouTube, Werbeseiten, Preprints, KI-Chatantworten und Seminarfolien sind **keine Forschungsbelege**. Online-Kataloge dürfen Metadaten liefern, aber nicht als Belege zitiert werden. Jede Quelle mit Prüf- und Volltextstatus, keine DOI-/Seitenzahlhalluzinationen. Review-Typ nach tatsächlicher Suche benennen.

Human Author: Student schreibt alles selbst. Agenten analysieren, kommentieren, helfen bei Quellen und reflektieren. Keine automatisch generierten abgabefertigen Absätze, Präsentationen oder Kapitel. Alle bedeutenden Entscheidungen benötigen Freigabe.

## Compliance: TEILWEISE_GEPRUEFT
Die beiden Seminar-PDFs enthalten einschlägige Regeln (u.a. KI nicht als Quelle und KI-Dokumentation im Kolloquium), aber **die spezifischen Moodle-Vorgaben und Bewertungsrubriken fehlen**. Eine generelle Erlaubnis zur KI-Textproduktion lässt sich aus den Folien nicht ableiten. Details in `00_admin/compliance_status.md`.

## Tests
```bash
python3 scripts/validate_research_data.py
python3 -m unittest discover -s tests -v
```
Validatoren prüfen CSV-/Dateistruktur, nicht den wissenschaftlichen Wahrheitsgehalt. Nach Anlage der Agenten ist je nach Claude-Code-Sitzung ein Neustart sinnvoll, damit neue Subagents erkannt werden.
