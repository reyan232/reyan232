# Private Ablage: offizielle Seminar- und Hochschulvorgaben

**Inhalt dieses Ordners wird NICHT in Git versioniert** (Ausnahmen: diese README und `originaldateien_sha256.txt`). Grund: Das Repository ist öffentlich, und der Foliensatz ist laut Folie 4 in Moodle passwortgeschützt. Hochschuleigene Dateien nicht ohne Erlaubnis öffentlich verteilen.

## Erwartete Originale (lokal ablegen)

| Datei | Herkunft | Status |
|---|---|---|
| `seminarfolien_WS_2026_27.pdf` | Originaldatei des Nutzers: `Seminar Digitalisierung des Finanzbereichs im Unternehmen_17c60eeaa0598d56257d813216a694a2.pdf` (63 PDF-Seiten) | vorhanden im Starterpaket; Phase 0 am 2026-11-07 gelesen |
| `seminarthemen_WS_2026_27.pdf` | Originaldatei des Nutzers: `Seminar Themen_WS 2026_27_5416485c69da232ecb5047313701d1d3.pdf` (1 PDF-Seite, Thema 9) | vorhanden im Starterpaket; Phase 0 am 2026-11-07 gelesen |

In einem frischen Git-Clone oder einer neuen Cloud-Sitzung fehlen die PDFs. Dann: Dateien aus dem Starterpaket hierher kopieren und prüfen:

```bash
cd 00_admin/hochschulregeln && sha256sum -c originaldateien_sha256.txt
```

Fehlen die Originale, darf kein Agent behaupten, sie gelesen zu haben; stattdessen den Studenten um die Dateien bitten.

**Wichtig:** Die Originale dienen der Kontrolle der Studien-, Prüfungs- und Themenvorgaben, nicht als wissenschaftliche Fachquellen über KI-Agenten. Foliennummern (aufgedruckt) ≠ PDF-Seitenposition, siehe `00_admin/seminar_requirements.md`.

## Noch fehlend – nach Erhalt hier ablegen und `/university-policy-check` ausführen
1. HaW Landshut: „Richtlinien für gute wissenschaftliche Praxis“ (Folie 67)
2. Fakultät BW: „Leitfaden für die Anfertigung einer Bachelorarbeit“ inkl. Hinweisen zum Plagiatsreport (Folie 59, 67; Homepage der Fakultät)
3. Prof. Dr. Dieses: „Vorgaben zur Anfertigung von wissenschaftlichen Arbeiten“ (Moodle-Kursraum „PROF. DR. DIESES: Informationen und Angebote für STUDIERENDE“ → „Bachelor's and Master's Thesis“)
4. Prof. Dr. Dieses: Bewertungskriterien Studienarbeit (ebenda)
5. ggf. gesonderte KI-Nutzungsregeln der Hochschule/Fakultät
6. Terminplan / Moodle-Ankündigungen; Nachweis der Themenzuteilung

Keine vollständige Compliance-Bestätigung vor Prüfung dieser Unterlagen.
