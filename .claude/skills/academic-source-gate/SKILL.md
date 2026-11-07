---
name: academic-source-gate
description: Prüft, ob Quellen als akademische Forschungsevidenz für diese Seminararbeit zugelassen sind.
---

## Regeln
- Erlaubt: peer-reviewte Journalartikel und Konferenzen, wissenschaftliche Fachbücher/Sammelbandbeiträge, überprüfbare Dissertationen.
- Nicht als Forschungsevidenz: Blogs, Video, Presse, Unternehmen, Wikipedia, Working Papers/Preprints, ungeprüfte Suchtreffer.
- Wissenschaftliche Dokumente dürfen online gefunden werden; Fundort-Webseiten sind nicht selbst die inhaltliche Evidenz.
- Trenne Metadatenprüfung, Publikationstypprüfung und Volltext-Aussage-Prüfung.
- Unverifizierte Kandidaten nicht in die akzeptierte Evidenzmatrix aufnehmen.

Ausgabe: `Quelle | Status | akademische Begründung | überprüfter Identifier | Zugriff | Ausschlussgrund/Prüflücke`.
Beispiel: `/academic-source-gate Prüfe diese fünf Literaturangaben.`

**Regeltypen strikt trennen:** Seminarunterlagen sind gültige **Aufgaben-/Zitierregelquellen**, nicht automatisch **akademische Forschungsevidenz** für Aussagen zu KI-Agenten. Ein hochschuleigener Leitfaden oder eine Bewertungsrubrik ist Regel-/Qualitätsmaßstab, kein Fachbeleg. KI-Chats sind laut Seminarfolien S. 65 und 77 grundsätzlich KEINE wissenschaftliche Quelle.
