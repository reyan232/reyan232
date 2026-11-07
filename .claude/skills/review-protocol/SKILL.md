---
name: review-protocol
description: Entwickelt und prüft ein nachvollziehbares Suchprotokoll mit Kriterien, Screening, Ausschlussgründen, Dublettenregeln und Synthese und bestimmt, ob die Recherche als systematisch oder nur als strukturiert bezeichnet werden darf. Verwenden bei Planung oder Kontrolle der Literatursuche, beim Führen von search_log.csv und screening_log.csv und vor dem Schreiben eines Methodikteils durch den Studenten.
---

# Review Protocol

## Vorgehen
1. Freigabestand prüfen (`00_admin/decision_log.md`): Forschungsfrage und Umfang 8–10 Seiten müssen vom Studenten bestätigt sein; sonst nur Entwurf.
2. Review-Typ transparent wählen (Vorschlag durch `methodology-advisor`); kein PRISMA-Anspruch ohne entsprechende Umsetzung; „systematisch“ nur bei dokumentierter, reproduzierbarer Datenbanksuche.
3. Datenbanken, exakte Suchstrings, Datum, Filter, Trefferzahlen mit Zählbasis in `02_search/search_log.csv` führen; Exporte lokal unter `02_search/exports/`.
4. Vorab definierte Ein- und Ausschlusskriterien (Codes in `02_search/search_protocol.md`, Freigabe nötig); jede Screening-Entscheidung mit Grund in `02_search/screening_log.csv`.
5. Dubletten dokumentieren; nur verifizierte akademische Literatur aufnehmen (`academic-source-gate`).
6. Evidenz nach Themen (`theme`) und Gegenbefunden (`related_evidence`) extrahieren; Risiken und Limitierungen benennen.
7. Reproduzierbarkeit testen: Könnte eine dritte Person mit Log + Protokoll dieselben Treffer erhalten? Lücken (z. B. fehlender Datenbankzugang) offen benennen.
8. `python3 scripts/validate_research_data.py` ausführen.

## Seminarthema 9
Suchstrings müssen neben KI-Agenten und realwirtschaftlicher Finanzfunktion auch konkrete Aufgabenfelder und Erfolgsfaktoren/Governance/Einführung abdecken. Nur wissenschaftliche Originale als Fachbelege. Bei unterentwickelter Evidenz zu Agenten in CFO-Funktionen die Aussage begrenzen, statt allgemeine RPA-/GenAI-Publikationen als Agentenbefunde umzudeuten.

## Ausgabe
`Protokollelement | Status (vorhanden/lückenhaft/fehlt) | Fundstelle in Projektdateien | Risiko für Reproduzierbarkeit | Aufgabe für Studenten | Freigabe nötig?` + empfohlene Bezeichnung des Review-Typs mit Begründung.

## Beispiel
`/review-protocol Prüfe, ob meine Recherche nachvollziehbar ist.`
`/review-protocol Darf ich meine Methode nach den bisherigen Suchläufen „systematisch“ nennen?`
