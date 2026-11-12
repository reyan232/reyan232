# Handoff – Academic Research Assistant „Finance AI Agents“

> Herkunft: KI-generiert (Claude Code, Orchestrator der Cloud-Sitzung, 2026-11-12) – Übergabedokument für die nächste Sitzung, nicht zur Abgabe.

**Zweck:** Die Arbeit in einer **lokalen** Claude-Code-Sitzung auf dem Rechner des Studenten fortsetzen. Dort sind die Chrome-Erweiterung (Zugriff auf die Hochschulbibliothek mit eigener Anmeldung) und der Download-Ordner erreichbar. Die Cloud-Sitzung konnte beides nicht.

Branch: `claude/finance-ai-agents-research-system-llfffr` · letzter Commit vor diesem Handoff: `948d041`

---

## 1. Lokales Setup (Student)

```bash
git clone https://github.com/reyan232/reyan232.git
cd reyan232
git checkout claude/finance-ai-agents-research-system-llfffr
```

Diese Dateien liegen bewusst **nicht** im öffentlichen Repo und müssen lokal ergänzt werden:

| Datei | Ziel | Quelle |
|---|---|---|
| Seminarfolien, Themenliste, Professorenvorgaben 10/2017, Bewertungsformular 2024 | `00_admin/hochschulregeln/` (Dateinamen siehe README dort) | eigene Ablage / Moodle |
| Fakultätsleitfaden 04/2024, HAW-Satzung GWP 2022 | `00_admin/hochschulregeln/` | Links in `00_admin/hochschulregeln/README.md` |
| KI-Nutzungsprotokoll (8 Einträge) | `00_admin/ki_nutzungsprotokoll.csv` | zuletzt im Chat gesendete Fassung |
| ZBW-Booklet (optional) | `04_quality/leitfaeden/` | Upload / econbiz.de |
| Heruntergeladene Fachartikel | `03_sources/pdfs/<source_id>.pdf` | Download-Ordner |

Integrität prüfen: `cd 00_admin/hochschulregeln && sha256sum -c originaldateien_sha256.txt`

Dann im Projektordner `claude` starten, mit `/agents` prüfen, dass die 6 Agenten geladen sind, und für die Bibliothek die Chrome-Verbindung mit `/chrome` aktivieren.

## 2. Startprompt für die neue Sitzung (kopieren)

```text
Lies HANDOFF.md, CLAUDE.md, 00_admin/decision_log.md und 01_scope/topic_options.md.
Prüfe mit `python3 scripts/validate_research_data.py` und `python3 -m unittest discover -s tests`, dass alles grün ist.
Dann: (1) Lies die PDFs in ~/Downloads, die zu Kandidaten in 03_sources/literature.csv passen oder neu sind,
kopiere sie nach 03_sources/pdfs/<source_id>.pdf, prüfe Metadaten mit scripts/crossref_lookup.py und
setze access_level nur für tatsächlich gelesene Texte auf VOLLTEXT_GELESEN; schreibe je Quelle eine
gekennzeichnete Kurznotiz nach 05_research_notes/. (2) Danach unterstütze mich bei der WISO/EBSCO-Suche
über meinen Bibliothekszugang in Chrome mit den Strings aus 02_search/suchstrings_phase1.md und protokolliere
jeden Lauf in 02_search/search_log.csv (echte Trefferzahlen, DATENBANK_GESAMT). Keine Massendownloads,
keine Themenentscheidung, kein Abgabetext. KI-Einsatz ins KI-Protokoll eintragen.
```

## 3. Projektstand

**Phase 0 – Hochschulregeln: erledigt, Status `TEILWEISE_GEPRUEFT`**
- Ausgewertet: Seminarfolien und Themenliste WS 2026/27, Professorenvorgaben (Stand 10/2017), Bewertungsformular (2024-01-02), Fakultätsleitfaden (04/2024), HAW-Satzung GWP (2022). Fundstellen und Rangfolge stehen in `00_admin/seminar_requirements.md`.
- Offen sind KI-Regeln für die schriftliche Arbeit (K1) und die Termine, deshalb nicht `GEPRUEFT`.

**Entscheidungen des Studenten** (Details in `00_admin/decision_log.md`)
- Thema Nr. 9 zugeteilt.
- Zweistufiges Quellen-Gate (K2 = Option B):
  - Stufe 1: peer-reviewte bzw. wissenschaftliche Literatur.
  - Stufe 2: Praxis-Fachzeitschriften laut Anhang 4 der Professorenvorgaben, mit CRAAP-Prüfung, nur ergänzend.
  - Der Validator erzwingt das über `AUFGENOMMEN_ERGAENZEND`.
- Zitierstil nach den Professorenvorgaben (K3): Fußnoten-Kurzbeleg „Vgl. Nachname (Jahr), S. x.“.

**Phase 1 – Themenfokus: Optionen vorgelegt, Entscheidung ausstehend**
- Option A: Autonomie- und Delegationsstufen als Ordnungsrahmen, Controlling + Rechnungswesen. Das ist die Empfehlung des methodology-advisor.
- Option B: Rechnungswesen.
- Option C: Controlling.
- Treasury wird nicht angeboten (Evidenz praktisch leer).
- Empfehlung: erst nach dem eigenen WISO/EBSCO-Durchgang entscheiden, aber vor dem Exposé.
- Vollberichte der Agenten: `05_research_notes/2026-11-07_phase1_*.md`. Übersicht: `01_scope/topic_options.md`.

**Daten** (Validator grün, 53 Tests grün)
- `03_sources/literature.csv`: 30 Einträge.
  - 22 KANDIDAT: 20 mit per Crossref verifizierten Metadaten, 2 WIDERSPRUECHLICH (Q008 wegen Platzhalterangaben im Crossref-Eintrag, Q014 wegen widersprüchlicher Verlagsangaben).
  - 8 AUSGESCHLOSSEN: Preprints, Working Papers, Masterarbeit.
  - Für alle gilt: Peer Review `UNKLAR`, Zugriff `NUR_METADATA`. Die Inhaltsangaben in `notes` stammen aus Suchmaschinen-Zusammenfassungen.
  - **Noch keine Quelle ist AUFGENOMMEN.**
- `02_search/search_log.csv`: 79 Läufe, alle WebSearch bzw. Crossref, also Vorrecherche. Die Datenbanksuche des Studenten fehlt noch. Freie IDs ab **S102**, Quellen-IDs ab **Q063**.
- `03_sources/evidence_matrix.csv`: leer, und das ist korrekt, solange keine Quelle aufgenommen ist.
- `04_quality/benchmark_register.csv`: B001 Bewertungsformular, B002 EconBiz-Lernpfade, B003 ZBW-Booklet.

## 4. Nächste Schritte (Reihenfolge)

1. **PDFs aus dem Download-Ordner einlesen** (siehe Startprompt). Q001 Resende 2025 hat Priorität: CC BY 4.0, PDF unter https://www.mdpi.com/2674-1032/4/4/65/pdf. Prüfen: Ist es ein Agent im engeren Sinn? Ist die Aufgabe Controlling oder Rechnungswesen? Wie ist das Experiment aufgebaut?
2. **WISO/EBSCO-Suche** mit `02_search/suchstrings_phase1.md`:
   - Stufe 1 und Stufe 2 getrennt protokollieren, Exporte nach `02_search/exports/`.
   - Stufe-2-Hinweis aus Folie 23: Baier/Tischler (2026), Controller Magazin 3/2026, S. 14–18.
3. **Peer-Review-Nachweise** für die verifizierten Kandidaten (Agent `citation-auditor`, Skill `academic-source-gate`). Fraglich sind besonders MDPI (Q001), IEEE Access (Q010), Inderscience (Q008), das BISE-Catchword (Q054) und das BPM-Forum (Q056).
4. **Entscheidung des Studenten:** Option A, B oder C; Teilbereich; Arbeitsdefinition „KI-Agent“ (D1–D3); Umgang mit Prüfungs-/Revisionsprototypen (Ausschluss oder gekennzeichnete Übertragung). Danach in `00_admin/decision_log.md` und `01_scope/` eintragen.
5. **Phase 2:** Forschungsfrage (formuliert der Student selbst), Review-Typ („strukturierte Literaturrecherche“), Zeitraum mit Ausnahmeregel für Grundlagenliteratur, Freigabe der Ausschlusscodes E1–E9 in `02_search/search_protocol.md`.

## 5. Klärungsbedarf für den Präsenztermin (keine E-Mail-Klärung, Folie 7)

1. Form der KI-Offenlegung in der Studienarbeit und welche KI-Nutzungen zulässig sind (K1).
2. Muss der Kopf des Bewertungsformulars auch bei der Studienarbeit beigefügt werden?
3. Müssen gesicherte Internetquellen mit abgegeben werden?
4. Termine: Exposé, Präsentations-Upload, Kolloquium, Abgabe.
5. Ggf.: Gehört die interne Revision zur CFO-Funktion?

## 6. Regeln und Fallstricke

- **Human-Author-Regel:** keine Abgabetexte. `06_student_draft/` ist für Claude gesperrt (`.claude/settings.json`).
- **Nichts erfinden.** Statuswerte: `NICHT_VERIFIZIERT` / `NUR_METADATA` / `NUR_ABSTRACT` / `VOLLTEXT_GELESEN`. Seitenangaben nur bei gelesenem Volltext; der Validator prüft das.
- **Metadaten prüfen:** `python3 scripts/crossref_lookup.py doi <DOI>` bzw. `search "<Titel>" --year <Jahr>`. Crossref belegt nur die Bibliografie, kein Peer Review.
- **Netzwerk:**
  - In der Cloud konnten Subagents per WebFetch keine Metadatendienste erreichen; lokal ist das voraussichtlich kein Problem.
  - MDPI blockt automatische Downloads (403). Nicht umgehen, sondern im Browser laden.
- **Bibliotheksdatenbanken:** normal suchen, keine automatisierten Massendownloads (Nutzungsbedingungen).
- **Öffentliches Repository:** keine PDFs, Exporte, Entwürfe, Feedback oder das KI-Protokoll committen; `.gitignore` deckt das ab.
- **Nach jedem Arbeitsgang:** Logs und CSVs pflegen, KI-Protokoll ergänzen, Validator ausführen, an den Studenten berichten (Pflichten in `CLAUDE.md`).

## 7. Cloud-Umgebung (falls wieder in der Cloud gearbeitet wird)

- Umgebung „reyan232 – Seminar-Recherche“ mit den erlaubten Hosts www.haw-landshut.de, www.econbiz.de, api.crossref.org, api.openalex.org, doi.org, www.mdpi.com und mdpi-res.com.
- In einer neuen Cloud-Sitzung fehlen alle lokalen Dateien aus Abschnitt 1. Sie müssen erneut hochgeladen werden.

## 8. Wichtige Dateien

| Datei | Inhalt |
|---|---|
| `CLAUDE.md` | Orchestrator-Regeln (werden automatisch geladen) |
| `00_admin/seminar_requirements.md` | Regelkatalog mit Fundstellen, Konflikte K1–K9 |
| `00_admin/compliance_status.md` | Compliance-Status, offene Fragen |
| `00_admin/decision_log.md` | alle Entscheidungen und Freigaben |
| `00_admin/datenmodell.md` | CSV-Spalten, Vokabular, Gates |
| `01_scope/topic_options.md` | Optionen A–C, Entscheidungsliste |
| `02_search/suchstrings_phase1.md` | Suchstrings für WISO/EBSCO |
| `04_quality/quality_rubric.md` | offizielle Bewertungskriterien + Prüffragen |
| `scripts/validate_research_data.py` | Validator |
| `scripts/crossref_lookup.py` | Metadatenprüfung |
