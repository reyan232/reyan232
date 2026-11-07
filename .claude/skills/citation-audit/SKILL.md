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

## Seminarspezifisch
Indirekte Quellenverweise beginnen mit „Vgl.“ (Folie 71); wörtliche Originaltreue nur bei Einsicht in die Textstelle prüfen; Sekundärzitate vermeiden bzw. „zitiert nach“ (Folie 70–72). KI ist keine Quelle (Folie 65, 77). Endgültige Zitiertechnik (Chicago/Harvard) erst nach den Professorenvorgaben festlegen.

## Grenzen
Keine Korrekturen am studentischen Text vornehmen und keine Ersatzformulierungen liefern – nur Befund, Fundstelle und Aufgabe für den Studenten.

## Ausgabe
`Prüfobjekt | Bibliografie | Typ/Peer Review | Beleg-Aussage | Fundstelle/Nachweis | Fehlerklasse | Nutzeraktion` + Liste offener Lücken.

## Beispiel
`/citation-audit Kontrolliere diese Behauptung anhand des beigefügten Papers.`
`/citation-audit Prüfe alle Belege in Abschnitt 3 von 06_student_draft/arbeit.md.`
