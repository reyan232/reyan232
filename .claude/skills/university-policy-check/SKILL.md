---
name: university-policy-check
description: Gleicht die ausgewerteten Regelwerke (Seminarfolien WS 2026/27, Professorenvorgaben, Bewertungsformular, Fakultätsleitfaden, HAW-Satzung GWP) mit neu nachgereichten Moodle-Dokumenten, Terminen und KI-Regeln ab, ordnet Regelebenen nach Spezifität, markiert Konflikte und holt vor Anwendung geänderter Regeln eine Freigabe ein. Verwenden, wenn neue Hochschuldokumente vorliegen, eine KI-Nutzung oder Formvorgabe auf Zulässigkeit geprüft werden soll oder der Compliance-Status aktualisiert werden muss.
---

# University Policy Check

## Ausgangslage
Ausgewertet (2026-11-07): Seminarfolien und Themenliste WS 2026/27 (Abgleich 1) sowie Professorenvorgaben 10/2017, Bewertungsformular 2024, Fakultätsleitfaden 04/2024 und HAW-Satzung GWP 2022 (Abgleich 2) – siehe `00_admin/seminar_requirements.md` und `00_admin/compliance_status.md`: **TEILWEISE_GEPRUEFT** (offen: KI-Regeln für die schriftliche Arbeit, Termine). Die PDFs liegen nur lokal in `00_admin/hochschulregeln/` (nicht in Git). Fehlen sie, den Studenten um die Dateien bitten und **nicht** behaupten, sie gelesen zu haben. Integrität: `sha256sum -c originaldateien_sha256.txt` im Ordner.

## Pflichtprüfung
1. Originaldokumente lesen und präzise Seiten/Abschnitte notieren. **Wörtliche explizite Anforderung** von Interpretation und offener Frage trennen.
2. Regelquelle und Spezifität zuordnen: HAW-Satzung gute wissenschaftliche Praxis < Fakultätsleitfaden BW < Vorgaben Prof. Dieses (Folie 67; V S. II) < Seminarfolien (für Studienarbeits-Details). Speziellere Regel hat Vorrang.
3. Prüfen: Themen-Nr. 9, CFO-Bereich Realwirtschaft, Exposé, Kolloquium/Thesenpapier (inkl. Fußzeile, KI-Folie, Kriterien Folie 58), 8–10 Seiten Textteil inkl. Abbildungen/Tabellen, physische/digitale Abgabe, Plagiatsreport, KI-Dokumentation.
4. **KI:** KI ist keine Quelle; Originalquellenpflicht. Die Pflicht zur KI-Transparenz im Kolloquium ist **keine generelle Erlaubnis** zum automatischen Schreiben. Zulässige/verbotene KI-Nutzungen bleiben `OFFEN`, bis ausdrückliche Regeln vorliegen.
5. **Zitate:** „Vgl.“ bei indirekten Zitaten; Sekundärzitate vermeiden; Formatwahl nach spezieller Regel statt zu raten.
6. **Konflikte** (auch mit `CLAUDE.md`, Quellen-Gate oder Agentenregeln, z. B. K1–K4): betroffenen Arbeitsschritt stoppen, Studenten informieren, nichts stillschweigend auflösen.
7. Neue Dokumente in `seminar_requirements.md` ergänzen; vor *wesentlichen* Änderungen an `CLAUDE.md`, Agenten oder Skills Nutzerfreigabe einholen; Entscheidung in `00_admin/decision_log.md`.
8. Status erst auf `GEPRUEFT` setzen, wenn alle in `00_admin/hochschulregeln/README.md` gelisteten Dokumente vorliegen und ausgewertet sind – und auch dann nie eine offizielle Genehmigung einer KI-Nutzung behaupten.

## Ausgabe
`Anforderung | Originalfundstelle | explizit / Interpretation | Status | Workflow-Folge | fehlende Originalvorschrift`; danach priorisierte Liste zur Nachreichung und Fragen für die nächste Präsenzveranstaltung (keine E-Mail-Klärung, Folie 7).

## Beispiel
`/university-policy-check Prüfe die neuen PDFs aus meinem Moodle-Kurs gegen die bestehenden Regeln.`
`/university-policy-check Darf ich laut den vorliegenden Regeln KI für die Literatursuche einsetzen?`
