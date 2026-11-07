---
name: academic-source-gate
description: Prüft nach dem zweistufigen Quellen-Gate, ob eine Quelle als Forschungsevidenz (Stufe 1 – peer-reviewte Zeitschrift oder Konferenz, wissenschaftliches Fachbuch oder Sammelband, überprüfbare Dissertation) oder als gekennzeichnete Ergänzung (Stufe 2 – Praxis-Fachzeitschrift laut Anhang 4 der Professorenvorgaben, mit CRAAP-Prüfung) zugelassen ist, und trennt Metadaten-, Publikationstyp- und Volltextprüfung. Verwenden, sobald eine Quelle, Literaturliste, URL oder ein Suchtreffer bewertet, in literature.csv aufgenommen oder in der Evidenzmatrix verwendet werden soll.
---

# Academic Source Gate

## Regeln (zweistufiges Gate, Entscheidung des Studenten vom 2026-11-07)
- **Stufe 1 – Forschungsevidenz (`AUFGENOMMEN`):** peer-reviewte Zeitschriftenartikel und tatsächlich begutachtete Konferenzbeiträge; wissenschaftliche Fachbücher/Monografien und Sammelbandbeiträge mit eindeutigem Verlag und Autorenschaft; Dissertationen mit überprüfbarem Hochschulnachweis (als Dissertation kennzeichnen, Evidenzniveau beachten).
- **Stufe 2 – ergänzend (`AUFGENOMMEN_ERGAENZEND`, `source_type = PRAXISBEITRAG`):** Beiträge aus Praxis-Fachzeitschriften, vorrangig aus der „Auswahl wissenschaftlicher Zeitschriften im Bereich Controlling/Finanzen“ der Professorenvorgaben (V Anhang 4, S. 25: u. a. Betriebs-Berater, BFuP, CFO aktuell, CFO Magazine, Controller Magazin, Controlling & Management Review, Controlling – Zeitschrift für erfolgsorientierte Unternehmenssteuerung, Corporate Finance, Der Betrieb, Risk/Compliance & Audit, Risiko Manager, zfbf, Zeitschrift für Bilanzierung, Rechnungswesen und Controlling, Zeitschrift für Corporate Governance, Zeitschrift für Internationale Rechnungslegung). Begutachtete Titel daraus (z. B. zfbf, BFuP) gehören bei Peer-Review-Nachweis in Stufe 1. Andere Praxiszeitschriften nur mit Einzelfreigabe des Studenten.
  - Pflicht: verifizierte Metadaten, Kennung/URL, dokumentierte **CRAAP-Prüfung** in `decision_reason` (Currency, Relevance, Authority, Audience, Purpose; ZBW-Booklet S. 13).
  - Verwendung nur für Praxisbeispiele, Verbreitung in der Praxis und aktuelle Entwicklungen; **nie alleiniger Beleg** für verallgemeinernde oder empirische Wirkungsaussagen; in der Evidenzmatrix `reliability` höchstens `MITTEL`, `limitations` Pflicht.
  - In der Arbeit werden Stufe-2-Quellen normal nach den Professorenvorgaben zitiert; die Stufenkennzeichnung ist projektintern.
- **Ausgeschlossen:** Blogs, Video/YouTube, Influencer, Presse, Unternehmens-/Anbietermarketing, Beratungs-Whitepaper, Wikipedia (laut Fakultätsleitfaden S. 7 unzulässig), Social Media, Working Papers/Preprints, ungeprüfte Suchtreffer, KI-Antworten. Ein Preprint wird nur durch seine begutachtete Endfassung ersetzt.
- Metadaten- und Suchdienste (Crossref, OpenAlex, Kataloge, Verlagsseiten, Suchmaschinen) dienen dem Finden und Verifizieren, sind aber selbst keine Belege.
- **Regeltypen strikt trennen:** Seminarunterlagen sind gültige Aufgaben-/Zitierregelquellen, keine Forschungsevidenz; Hochschulrubriken und Schreibleitfäden sind Qualitätsmaßstäbe, keine Fachbelege; Vorbildarbeiten sind keine automatisch akzeptierte Evidenz. KI-Chats sind laut Seminarfolien Folie 65 und 77 grundsätzlich keine Quelle.

## Ablauf
1. Publikationstyp und Stufe bestimmen (Vokabular `source_type` in `00_admin/datenmodell.md`).
2. Metadaten gegen mindestens einen zuverlässigen Nachweis prüfen → `metadata_status`, `metadata_evidence`.
3. Peer Review nur mit Nachweis (Begutachtungsrichtlinie) → `peer_review_status`, `peer_review_evidence`. DOI ≠ Peer Review.
4. Integrität prüfen (Retraction, Korrektur, Kontroverse) → `integrity_flags`.
5. Zugriff ehrlich angeben: `NUR_METADATA` / `NUR_ABSTRACT` / `VOLLTEXT_GELESEN`.
6. Bei Stufe 2: CRAAP-Prüfung stichwortartig in `decision_reason` dokumentieren; Zeitschrift gegen Anhang 4 abgleichen.
7. Unverifizierte Kandidaten bleiben `KANDIDAT`/`NICHT_VERIFIZIERT` und dürfen nicht in die Evidenzmatrix.
8. Nach Eintrag: `python3 scripts/validate_research_data.py` (erzwingt beide Gates).

## Ausgabe
`Quelle | Typ | Stufe (1 / 2 / ausgeschlossen / ungeklärt) | akademische Begründung | überprüfter Identifier + Nachweis | Zugriff | Ausschlussgrund oder Prüflücke`

## Beispiel
`/academic-source-gate Prüfe diese fünf Literaturangaben.`
`/academic-source-gate Ist dieser Konferenzbeitrag peer-reviewed oder nur ein Preprint?`
`/academic-source-gate Darf dieser Controller-Magazin-Artikel als Stufe-2-Quelle aufgenommen werden?`
