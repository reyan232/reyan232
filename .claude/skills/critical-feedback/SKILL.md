---
name: critical-feedback
description: COACH- oder EXAMINER-Review studentischer Texte (Entwurf, Gliederung, Exposé, Thesen, Folien) ohne Ghostwriting – jeder Befund mit Stelle, Schweregrad, Begründung und Selbstkorrekturauftrag, keine Ersatzabsätze. Verwenden, wenn der Student Feedback, Kritik, eine Probe-Begutachtung oder Verbesserungshinweise zu eigenem Text wünscht. Nutzt den Subagenten scientific-critic.
---

# Critical Feedback

## Modi
- `COACH` (Standard): zugänglich erklären, Leitfragen stellen, selbst lösbare Verbesserungsschritte priorisieren.
- `EXAMINER`: streng auf Argumentationsfehler, Quellenrisiken und Methodiklücken prüfen; ausdrücklich Simulation, keine echte Notengebung.

## Ablauf
1. Hochschulregeln prüfen (`00_admin/compliance_status.md`): Bei Bitte um „Textverbesserung“ standardmäßig nur Randkommentare und Satz-für-Satz-Hinweise, keine umgeschriebenen Absätze.
2. `scientific-critic` mit Modus, Datei und Fokus beauftragen (liest `06_student_draft/` nur).
3. Für jeden Befund: konkrete Stelle, Schweregrad, Begründung (Folie/Regel), Selbstkorrekturauftrag.
4. Bericht unter `07_feedback/JJJJ-MM-TT_<MODUS>_<gegenstand>.md` mit Zeile `> Herkunft: KI-generiert (scientific-critic, MODUS, Datum) – Feedback, kein Abgabetext` ablegen.
5. KI-Nutzung in `00_admin/ki_nutzungsprotokoll.csv` eintragen.

## Seminarpflicht
Separat beide Elemente aus Thema 9 prüfen: konkrete KI-Agenten-Use-Cases **und** Erfolgsfaktoren zur Schaffung einer einsatzfähigen Basis im Unternehmen. Außerdem Praxisumsetzung, Effizienz vs. Effektivität, begrenzte Beleglage, Synthese statt Aneinanderreihung (Folie 90), keine Ich-Form (Folie 88). Arbeite nach `00_admin/requirements_checklist.md`, ohne fremden Arbeitstext zu produzieren.

## Beispiel
`/critical-feedback EXAMINER Bewerte meinen selbst geschriebenen Diskussionsteil in 06_student_draft/kapitel4.md.`
`/critical-feedback COACH Ist meine Gliederung logisch aufgebaut?`
