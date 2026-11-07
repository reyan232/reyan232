---
name: citation-audit
description: Gleicht Bibliografie, Kennungen (DOI, ISBN, URN, Hochschulnachweis), Fundstellen und Aussage-Beleg-Passung ab, prüft Zitatgenauigkeit, Dubletten und Retraktionen und listet offene Lücken. Verwenden, wenn Literaturangaben, library.bib, die Evidenzmatrix oder die Belege eines studentischen Entwurfs kontrolliert werden sollen. Nutzt den Subagenten citation-auditor.
---

# Citation Audit

## Prüfprozess
1. Existenz der Publikation über nachvollziehbaren Primär- bzw. Metadatennachweis bestätigen.
2. DOI, ISBN, URN, Autoren, Jahr, Journal/Verlag abgleichen; Peer Review nicht aus der DOI ableiten.
3. Fundstelle nur vergeben, wenn der einschlägige Originaltext tatsächlich vorliegt (`VOLLTEXT_GELESEN`).
4. Aussage-Quelle-Passung als `GEPRUEFT`, `TEILWEISE`, `NICHT_PRUEFBAR` oder `FALSCH` kennzeichnen; in `evidence_matrix.csv` als `verified_against_text` = `JA` / `TEILWEISE` / `NEIN`.
5. Fehlende Seiten, nicht erreichbare Volltexte (Fernleihe empfehlen, Folie 72), Retraktionen und Dubletten melden.
6. `library.bib`-Keys müssen `source_id`s mit `metadata_status = VERIFIZIERT` sein.
7. Abschließend `python3 scripts/validate_research_data.py` ausführen und Ergebnis berichten.

## Verbindliche Zitierweise (Professorenvorgaben „V“, Stand 10/2017, S. 10–16; vom Studenten bestätigt 2026-11-07)
- **Fußnoten mit Kurzbeleg:** „Vgl. Nachname (Jahr), S. x.“ bei sinngemäßen Zitaten; wörtliche Zitate (nur ausnahmsweise) ohne „Vgl.“; Fußnoten 10 pt, einzeilig; Verlag nicht in der Fußnote (L S. 6).
- Mehrere Autoren mit „/“ ohne Leerzeichen; mehr als drei → „u. a.“ bzw. „et al.“; mehrere Quellen in einer Fußnote durch Semikolon, Reihenfolge wie im Literaturverzeichnis.
- Genaue Seitenangaben; Bis-Strich als Gedankenstrich ohne Leerzeichen („S. 13–17“); **„f.“/„ff.“, „ebenda“, „a. a. O.“ unzulässig**.
- Autorennamen im Fließtext in Großbuchstaben; Stellung der Fußnote nach V S. 13.
- Auslassungen/Ergänzungen in wörtlichen Zitaten nach Folie 70 („[.]“, „[…]“, „[ ]“, „[sic!]“).
- Sekundärzitat nur als Notbehelf (Fernleihe zumutbar): Fußnote nennt das Original, Literaturverzeichnis „…, zitiert nach: …“ (V S. 12).
- **Literaturverzeichnis:** alle zitierten öffentlich zugänglichen Quellen; Verfasser + Jahr **fett**; erster Vorname ausgeschrieben; „Titel. Untertitel“; Auflage vor Ort; Ort: Verlag; Zeitschriften „in: Titel, Jg./Vol., Heft/No./Issue, S. x–y.“; Internetquellen mit URL und (Sichtungsdatum); jede Angabe endet mit Punkt; Leerzeile zwischen Einträgen; alphabetisch, keine Trennung nach Quellenart; gleiche Autoren chronologisch mit a/b/c (V S. 13–16).
- Abbildungen/Tabellen: „Quelle: Nachname (Jahr), S. x.“, „Quelle: in Anlehnung an …“, „Quelle: eigene Darstellung.“ (V S. 7–8).
- KI ist keine Quelle (Folie 65, 77); KI-gestützte Inhalte nur mit zutreffendem Originalnachweis; Offenlegung des KI-Einsatzes nach K1 (`00_admin/seminar_requirements.md`).
- Zotero-/BibTeX-Exporte erzeugen dieses Format nicht automatisch – Abweichungen als Formfehler melden.

## Grenzen
Keine Korrekturen am studentischen Text vornehmen und keine Ersatzformulierungen liefern – nur Befund, Fundstelle und Aufgabe für den Studenten.

## Ausgabe
`Prüfobjekt | Bibliografie | Typ/Peer Review | Beleg-Aussage | Fundstelle/Nachweis | Fehlerklasse | Nutzeraktion` + Liste offener Lücken.

## Beispiel
`/citation-audit Kontrolliere diese Behauptung anhand des beigefügten Papers.`
`/citation-audit Prüfe alle Belege in Abschnitt 3 von 06_student_draft/arbeit.md.`
`/citation-audit Entspricht mein Literaturverzeichnis den Professorenvorgaben?`
