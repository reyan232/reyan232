# Academic Research Assistant – Finance AI Agents

Projektlokales Claude-Code-Multi-Agenten-System zur **Unterstützung** (nicht zum Schreiben) einer Bachelor-Studienarbeit im Seminar „Digitalisierung des Finanzbereichs im Unternehmen“, WS 2026/27, Prof. Dr. Patrick Dieses, Hochschule Landshut.

- Arbeitsannahme: Thema **Nr. 9 „Einsatz von KI-Agenten in der Finanzfunktion: Use Cases und Erfolgsfaktoren“** (Moodle-Vergabe noch zu bestätigen)
- Umfang: **8–10 Seiten Textteil inkl. Abbildungen/Tabellen**
- Scope: **CFO-Funktion realwirtschaftlicher Unternehmen**, nicht Banken/Finanzindustrie
- Compliance-Status: **TEILWEISE_GEPRUEFT** (`00_admin/compliance_status.md`)

> Die Hauptkonversation ist der Orchestrator. Sechs echte Subagents recherchieren und prüfen, sieben Skills liefern wiederverwendbare Prüfabläufe. Der Student trifft alle wissenschaftlichen Entscheidungen und formuliert jeden Abgabetext selbst.

## Einstieg
1. Projektordner öffnen und `claude` starten. **Nach dem ersten Anlegen von `.claude/agents/` Claude Code neu starten**, damit die Subagents erkannt werden (Prüfen mit `/agents`).
2. Seminar-PDFs lokal nach `00_admin/hochschulregeln/` legen (nicht in Git) und Integrität prüfen: `cd 00_admin/hochschulregeln && sha256sum -c originaldateien_sha256.txt`.
3. Fehlende Unterlagen (HaW-Richtlinie, Fakultätsleitfaden, Professorenvorgaben, Bewertungskriterien, ggf. KI-Regeln) in denselben Ordner legen und `/university-policy-check` ausführen.
4. Bestätigen, dass Thema 9 zugeteilt wurde – erst dann Themenfokussierung (Phase 1).
5. KI-Protokoll anlegen, falls nicht vorhanden: `cp 00_admin/ki_nutzungsprotokoll.vorlage.csv 00_admin/ki_nutzungsprotokoll.csv`.

## Projektablauf
| Phase | Inhalt | Wer entscheidet |
|---|---|---|
| 0 | Hochschulregeln lesen und abgleichen | Student bestätigt Abgleich |
| 1 | ≤ 3 eng umrissene Themenoptionen mit Chancen, Literatur, Risiken | **Student** |
| 2 | Forschungsfrage, Kriterien, Such- und Auswahlkonzept als Vorschlag | **Student** gibt frei |
| 3 | Dokumentierte Recherche, Dublettenprüfung, Screening, Verifikation | Agenten (autonom, protokolliert) |
| 4 | Kurznotizen, Evidenzmatrix, Gegenbefunde, Lücken | Agenten + Student |
| 5 | **Student schreibt**; Feedback zu Argumentation, Struktur, Methodik, Zitierfähigkeit | Student |
| 6 | Qualitätssicherung → priorisierte To-do-Liste | Student setzt um |

## Freigaben
Ohne Einzelfreigabe: Recherche, Prüfung, Protokolle, Notizen, Feedbackberichte.
Nur mit ausdrücklicher Freigabe (dokumentiert in `00_admin/decision_log.md`): Thema/Eingrenzung, Forschungsfrage, Gliederung, Methodik, Zitierstil, Änderungen an studentischem Text, externe Accounts/Käufe, neue MCP-Server, wesentliche Änderungen an Regeln/Agenten/Skills.

## Agenten (`.claude/agents/`, nur lesend)
| Agent | Aufgabe |
|---|---|
| `source-researcher` | zulässige wissenschaftliche Literatur finden, Suchwege offenlegen |
| `citation-auditor` | Bibliografie, Kennungen, Beleg-Aussage-Passung prüfen |
| `methodology-advisor` | Forschungsfrage, Kriterien, Suchprotokoll, Synthese (Vorschläge) |
| `finance-ai-expert` | Agentenbegriff, Abgrenzung zu RPA/Chatbots, Finance-Anwendungen, Evidenzlage |
| `scientific-critic` | Feedback zu Studententexten: `COACH` oder `EXAMINER` |
| `quality-controller` | Rubriken und überprüfbare Vorbildarbeiten → Kriterien-Checklisten |

## Skills (`.claude/skills/`)
`university-policy-check`, `seminar-deliverables`, `academic-excellence`, `academic-source-gate`, `review-protocol`, `citation-audit`, `critical-feedback` – automatisch nutzbar oder manuell per `/name`.

## Beispielbefehle
```text
/university-policy-check Prüfe die neuen PDFs aus Moodle gegen die bestehenden Regeln.
Nutze den methodology-advisor und den finance-ai-expert: drei eng umrissene Themenoptionen für Thema 9 mit Risiken – keine Entscheidung.
Nutze den source-researcher für eine erste Sondierung zu "agentic AI" im Controlling; danach citation-auditor. Alles protokollieren.
/academic-source-gate Prüfe diese fünf Literaturangaben.
/seminar-deliverables EXPOSE Prüfe meine eigene Exposé-Gliederung gegen Folie 54.
/critical-feedback EXAMINER 06_student_draft/kapitel2.md
/citation-audit Kontrolliere die Belege in Abschnitt 3 meines Entwurfs.
```

## Struktur
```
CLAUDE.md                      Orchestrator-Regeln (dauerhaft geladen)
.claude/agents/ | skills/      6 Subagents, 7 Skills; settings.json = Schreibschutz 06_student_draft/
00_admin/                      Regelkatalog, Compliance, Checkliste, Entscheidungen, Datenmodell, KI-Protokoll
01_scope/                      Themenoptionen, Forschungsfrage (Platzhalter)
02_search/                     Suchprotokoll, Such- und Screening-Log, exports/ (lokal)
03_sources/                    Quellenregister, Evidenzmatrix, library.bib, pdfs/ (lokal)
04_quality/                    Benchmark-Register, Rubrik, reports/ (lokal)
05_research_notes/             KI-gestützte Notizen – nicht zur Abgabe
06_student_draft/              nur studentischer Text (lokal, gesperrt für Claude)
07_feedback/                   Coach-/Examiner-Berichte (lokal)
scripts/, tests/               Validator und Tests
STARTPROMPT.md                 ursprünglicher Bootstrap-Prompt (Starterpaket v3)
```

## Tests und Validierung
```bash
python3 scripts/validate_research_data.py          # Daten + Projektstruktur
python3 scripts/validate_research_data.py --strict # Hinweise als Fehler
python3 -m unittest discover -s tests -v
```
Geprüft werden CSV-Spalten und Vokabular, das Aufnahme-Gate für Quellen, Beleg-Fundstellen (keine Seitenangaben ohne Volltext), Noten nur mit Nachweis, BibTeX-Zuordnung, Herkunftskennzeichnung von Notizen, YAML-Frontmatter der Agenten/Skills, nur-lesende Agenten-Tools und der Schreibschutz. **Nicht** geprüft wird die fachliche Richtigkeit. Optional: PyYAML für strenge YAML-Prüfung (sonst einfacher Fallback-Parser).

## Datenschutz
Dieses Repository ist **öffentlich** (`reyan232/reyan232`, zugleich GitHub-Profil-Repository). Per `.gitignore` bleiben lokal: Seminar- und Hochschul-PDFs (Moodle-passwortgeschützt), Volltexte, Datenbank-Exporte, `06_student_draft/`, `07_feedback/`, `04_quality/reports/`, das reale KI-Nutzungsprotokoll, `00_admin/privat/` und `.claude/settings.local.json`. Diese Dateien gehen beim Ende einer Cloud-Sitzung verloren, wenn sie nicht lokal gesichert werden. **Empfehlung:** das Projekt in ein privates Repository verschieben; ein Merge in den Standard-Branch würde diese README zudem auf dem öffentlichen GitHub-Profil anzeigen.
