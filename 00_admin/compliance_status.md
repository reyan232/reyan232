# Hochschul-/KI-Compliance

**Status: TEILWEISE_GEPRUEFT – Regelwerke weitgehend vollständig; offen: KI-Regeln für die schriftliche Arbeit, Termine, Themenzuteilung**

> Herkunft: gemischt – Starterpaket v3 + KI-gestützte Abgleiche 1 und 2 (Claude Code, 2026-11-07). Internes Prüfprotokoll, **keine Bescheinigung der Hochschule** und **keine Genehmigung einer konkreten KI-Nutzung**.

## Phase 0 – geprüft am 2026-11-07
- Die beiden studentisch bereitgestellten PDFs (Seminarfolien „Digitalisierung des Finanzbereichs im Unternehmen“ WS 2026/27; „Seminar Themen_WS 2026_27“) wurden im Projekt selbst gelesen (Textextraktion aller 63 Seiten, Sichtprüfung Themenliste) und mit `00_admin/seminar_requirements.md` abgeglichen. SHA256 stimmt mit `00_admin/hochschulregeln/originaldateien_sha256.txt` überein.
- Ergebnis: Kernangaben bestätigt; Ergänzungen/Korrekturen und Konfliktpunkte K1–K4 in `00_admin/seminar_requirements.md`.
- Diese Unterlagen sind verbindlich zu prüfende **Aufgabengrundlage**, aber keine akademischen Forschungsbelege.

## Abgleich 2 – nachgereichte Regelwerke, geprüft am 2026-11-07
- Gelesen: Professorenvorgaben für wissenschaftliche Arbeiten (Stand 10/2017), Bewertungsformular (Stand 2024-01-02), Fakultätsleitfaden Bachelorarbeit (Stand 04/2024, abgerufen von haw-landshut.de), HAW-Satzung gute wissenschaftliche Praxis (Fassung 28.11.2022, abgerufen von haw-landshut.de). Prüfsummen in `00_admin/hochschulregeln/originaldateien_sha256.txt`.
- Ergebnis: Rangfolge Satzung < Fakultätsleitfaden < Professorenvorgaben < Seminarfolien (Studienarbeit); Formalia, Zitierweise (K3 aufgelöst) und Bewertungskriterien geklärt; K5–K9 durch Rangregel aufgelöst; K1 teilweise geklärt; K2 erfordert Entscheidung. Details: `00_admin/seminar_requirements.md`.
- Warum weiterhin TEILWEISE_GEPRUEFT: keine ausdrückliche Regel zu zulässigen KI-Nutzungen und zur KI-Offenlegung in der *schriftlichen* Studienarbeit (nur L S. 7: KI-Quellen „stets auszuweisen“); Termine und Themenzuteilung fehlen; Modulbeschreibung/Prüfungsordnung nicht vorliegend.

## Bekannte Regeln (aus den beiden Seminar-PDFs)
Thema Nr. 9 und Aufgabenstellung; realwirtschaftlicher CFO-Bereich; 8–10 Textseiten inkl. Abbildungen/Tabellen; Exposé, Kolloquium (inkl. Bewertungskriterien Folie 58) und Studienarbeit; KI ist keine Quelle, Nachweise nur an wissenschaftlichen Originalquellen; „Vgl.“ bei indirekten Zitaten; Sekundärzitate vermeiden (Fernleihe zumutbar); Angabe der KI-Tools für Studienarbeit und Präsentation im Kolloquium (Folie 56); Fragenklärung nur in Veranstaltungen (Folie 7).

## Ergänzende Regeln aus Abgleich 2 (Auszug)
Fußnoten-Kurzbeleg „Vgl. Nachname (Jahr), S. x.“, keine „ff.“/„ebenda“/„a. a. O.“ (V S. 10–11); Times New Roman 12 pt, 1,5-zeilig, Ränder 2,0/1,5/3,0/1,5 cm (V S. 5, L S. 4); kein Abstract und keine eidesstattliche Erklärung bei der Studienarbeit (V S. 4); Hauptteil ≥ ¾ des Textes, max. 3 Gliederungsebenen (V S. 6–7); Wikipedia unzulässig (L S. 7); KI-Quellen „stets auszuweisen“ (L S. 7); Plagiatsprüfung mit PlagAware (L S. 7); erfundene Quellen/Belege = wissenschaftliches Fehlverhalten (G § 11).

## Noch nicht gesichert
- Abschließende Zulässigkeit einzelner KI-Nutzungen und Form der KI-Offenlegung in der schriftlichen Arbeit (K1).
- Aktuelle Termine (Exposé, Präsentations-Upload, Kolloquium, Abgabe).
- Bestätigung der Moodle-Vergabe von Thema 9.

Eine KI-Dokumentationsfolie bedeutet **nicht**, dass KI-Ghostwriting erlaubt ist. Bis zur Klärung gilt die restriktive Human-Author-Regel (`CLAUDE.md`).

## Klärungsbedarf für die nächste Präsenzveranstaltung (keine E-Mail-Klärung, Folie 7)
1. Bestätigung der Themenzuteilung Nr. 9 (falls Moodle nicht eindeutig).
2. Erwartete Form der KI-Offenlegung in der Studienarbeit und zulässige KI-Nutzungen (K1; L S. 7 verlangt Ausweis von KI-Quellen, Folien verbieten KI als Quelle).
3. Ist das Bewertungsformular (Kopf „vom Verfasser zu befüllen“) auch bei der Studienarbeit beizufügen? (V S. II nennt nur BA/MA.)
4. Sind gesicherte Kopien der Internetquellen bei der Studienarbeit mit abzugeben? (V S. 16 für BA/MA: CD.)
5. Termine: Exposé, Präsentations-Upload, Kolloquium, Abgabe.

## Datenschutz / Vertraulichkeit (technische Vorkehrung, Freigabe durch Studenten ausstehend)
Das Git-Repository `reyan232/reyan232` ist **öffentlich**. Deshalb werden per `.gitignore` **nicht** versioniert: Seminar-PDFs und weitere Hochschuldokumente (Moodle-passwortgeschützt, Folie 4; auch Professorenvorgaben, Bewertungsformular, Fakultätsleitfaden und Satzung – nur Prüfsummen und Bezugsquellen werden versioniert), Schreibleitfäden-PDFs, Volltext-PDFs, Datenbank-Exporte, `06_student_draft/`, Feedback- und Qualitätsberichte zum Entwurf, das reale KI-Nutzungsprotokoll und lokale Claude-Einstellungen. Empfehlung: Projekt in ein **privates** Repository verschieben.

## Pflicht vor Einreichung
- Noch fehlende Dokumente (KI-Regeln, Termine) einlesen (`/university-policy-check`); speziellere Vorschriften haben Vorrang.
- KI-Einsatzaufzeichnungen (`00_admin/ki_nutzungsprotokoll.csv`) abgleichen und Offenlegungsanforderungen bestätigen.
- Zitierweise, Plagiatsreport, Layout, Abgabetermin und Kopienregelung gegen Originalrichtlinien prüfen.
