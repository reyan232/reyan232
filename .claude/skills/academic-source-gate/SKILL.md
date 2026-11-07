---
name: academic-source-gate
description: Prüft, ob eine Quelle als akademische Forschungsevidenz für diese Seminararbeit zugelassen ist (peer-reviewte Zeitschrift oder Konferenz, wissenschaftliches Fachbuch oder Sammelband, überprüfbare Dissertation) und trennt Metadaten-, Publikationstyp- und Volltextprüfung. Verwenden, sobald eine Quelle, Literaturliste, URL oder ein Suchtreffer bewertet, in literature.csv aufgenommen oder in der Evidenzmatrix verwendet werden soll.
---

# Academic Source Gate

## Regeln
- **Erlaubt als Forschungsevidenz:** peer-reviewte Zeitschriftenartikel und tatsächlich begutachtete Konferenzbeiträge; wissenschaftliche Fachbücher/Monografien und Sammelbandbeiträge mit eindeutigem Verlag und Autorenschaft; Dissertationen mit überprüfbarem Hochschulnachweis (als Dissertation kennzeichnen, Evidenzniveau beachten).
- **Nicht als Forschungsevidenz:** Blogs, Video/YouTube, Influencer, Presse, Unternehmens-/Anbietermarketing, Beratungs-Whitepaper, Wikipedia, Social Media, Working Papers/Preprints, ungeprüfte Suchtreffer, KI-Antworten. Ein Preprint wird nur durch seine begutachtete Endfassung ersetzt.
- Metadaten- und Suchdienste (Crossref, OpenAlex, Kataloge, Verlagsseiten, Suchmaschinen) dienen dem Finden und Verifizieren, sind aber selbst keine Belege.
- **Regeltypen strikt trennen:** Seminarunterlagen sind gültige Aufgaben-/Zitierregelquellen, keine Forschungsevidenz; Hochschulrubriken und Schreibleitfäden sind Qualitätsmaßstäbe, keine Fachbelege; Vorbildarbeiten sind keine automatisch akzeptierte Evidenz. KI-Chats sind laut Seminarfolien Folie 65 und 77 grundsätzlich keine Quelle.
- **Praxisfachzeitschriften** (z. B. Controller Magazin): derzeit ausgeschlossen; offener Konfliktpunkt K2 in `00_admin/seminar_requirements.md` – Entscheidung des Studenten abwarten.

## Ablauf
1. Publikationstyp bestimmen (Vokabular `source_type` in `00_admin/datenmodell.md`).
2. Metadaten gegen mindestens einen zuverlässigen Nachweis prüfen → `metadata_status`, `metadata_evidence`.
3. Peer Review nur mit Nachweis (Begutachtungsrichtlinie) → `peer_review_status`, `peer_review_evidence`. DOI ≠ Peer Review.
4. Integrität prüfen (Retraction, Korrektur, Kontroverse) → `integrity_flags`.
5. Zugriff ehrlich angeben: `NUR_METADATA` / `NUR_ABSTRACT` / `VOLLTEXT_GELESEN`.
6. Unverifizierte Kandidaten bleiben `KANDIDAT`/`NICHT_VERIFIZIERT` und dürfen nicht in die Evidenzmatrix.
7. Nach Eintrag: `python3 scripts/validate_research_data.py` (erzwingt das Gate für `AUFGENOMMEN`).

## Ausgabe
`Quelle | Typ | Status (zulässig / unzulässig / ungeklärt) | akademische Begründung | überprüfter Identifier + Nachweis | Zugriff | Ausschlussgrund oder Prüflücke`

## Beispiel
`/academic-source-gate Prüfe diese fünf Literaturangaben.`
`/academic-source-gate Ist dieser Konferenzbeitrag peer-reviewed oder nur ein Preprint?`
