# Private Ablage: offizielle Seminar- und Hochschulvorgaben

**Inhalt dieses Ordners wird NICHT in Git versioniert** (Ausnahmen: diese README und `originaldateien_sha256.txt`). Grund: Das Repository ist öffentlich; der Foliensatz ist laut Folie 4 in Moodle passwortgeschützt, und auch frei abrufbare Hochschuldokumente werden nicht weiterverteilt.

## Vorhandene Originale (lokal ablegen; Stand 2026-11-07 gelesen)

| Datei (lokal) | Inhalt | Bezugsquelle | Ausgewertet |
|---|---|---|---|
| `seminarfolien_WS_2026_27.pdf` | Seminarfolien WS 2026/27 (63 PDF-Seiten), Original: `Seminar Digitalisierung des Finanzbereichs im Unternehmen_17c60eeaa0598d56257d813216a694a2.pdf` | Moodle (Starterpaket) | Abgleich 1 |
| `seminarthemen_WS_2026_27.pdf` | Themenliste (1 Seite), Original: `Seminar Themen_WS 2026_27_5416485c69da232ecb5047313701d1d3.pdf` | Moodle (Starterpaket) | Abgleich 1 |
| `prof_vorgaben_wiss_arbeiten_2017-10.pdf` | Prof. Dieses: Vorgaben zur Anfertigung von wissenschaftlichen Arbeiten, Stand 10/2017 (40 Seiten) | Upload des Studenten (Moodle/Homepage Prof. Dieses) | Abgleich 2 |
| `prof_bewertung_wiss_arbeiten_2024-01-02.pdf` | Prof. Dieses: Formular „Bewertung wissenschaftlicher Arbeiten“, Stand 2024-01-02 (1 Seite) | Upload des Studenten | Abgleich 2 |
| `fakultaet_bw_leitfaden_bachelorarbeit_2024-06-25.pdf` | Fakultät BW: Leitfaden Bachelorarbeit, Fußzeile „Stand: 04/2024“ (12 Seiten) | https://www.haw-landshut.de/static/Fakultaet_BW/1_Studium/4_Laufender_Studienbetrieb/6_Abschlussarbeiten/Leitfaden_Bachelorarbeit_Stand_25.06.2024.pdf | Abgleich 2 |
| `haw_satzung_gute_wiss_praxis_2022-11-28.pdf` | HAW Landshut: Satzung zur Sicherung guter wissenschaftlicher Praxis, Fassung 28.11.2022 (16 Seiten) | https://www.haw-landshut.de/static/Justiziariat/2022/kF/317-1_Satzung-gute-wissenschaftliche-Praxis_28112022.pdf (verlinkt auf haw-landshut.de/forschung/wir-ueber-uns) | Abgleich 2 |

In einem frischen Git-Clone oder einer neuen Cloud-Sitzung fehlen die PDFs. Dann: Moodle-Dateien aus eigener Ablage hierher kopieren, öffentliche Dokumente über die Links neu laden und prüfen:

```bash
cd 00_admin/hochschulregeln && sha256sum -c originaldateien_sha256.txt
```

Fehlen die Originale, darf kein Agent behaupten, sie gelesen zu haben; stattdessen den Studenten um die Dateien bitten. Weicht eine Prüfsumme ab (z. B. neue Fassung), `/university-policy-check` erneut ausführen.

**Wichtig:** Die Dokumente dienen der Kontrolle der Studien-, Prüfungs- und Formvorgaben, nicht als wissenschaftliche Fachquellen über KI-Agenten. Auswertung und Rangfolge: `00_admin/seminar_requirements.md`.

## Noch fehlend
1. Ausdrückliche Regeln zu zulässigen KI-Nutzungen und zur KI-Offenlegung in der schriftlichen Studienarbeit (falls vorhanden: Moodle, Modulbeschreibung, Prüfungsordnung)
2. Terminplan / Moodle-Ankündigungen (Exposé, Präsentations-Upload, Kolloquium, Abgabe)
3. Nachweis der Themenzuteilung Nr. 9
4. optional: Modulbeschreibung des Seminars, Allgemeine Prüfungsordnung (vom Leitfaden S. 8 genannt)

Keine vollständige Compliance-Bestätigung vor Prüfung dieser Unterlagen.
