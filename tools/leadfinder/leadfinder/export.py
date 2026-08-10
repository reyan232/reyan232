"""CSV-Ausgabe.

Zwei Entscheidungen sind auf deutsches Excel gemünzt: Semikolon als Trenner
und UTF-8 *mit* BOM. Ohne BOM zeigt Excel "Bäckerei" als "BÃ¤ckerei" — die
Datei wäre technisch korrekt und praktisch unbrauchbar.

Beide Datenquellen verlangen einen Hinweis, aus unterschiedlichen Gründen:
OSM per Lizenz (ODbL-Namensnennung), Google per Nutzungsbedingungen
(Speicherbeschränkung). Statt einer Kommentarzeile, die jeden CSV-Parser
stört, trägt jede Zeile eine Spalte `quelle`; die Auflagen stehen in einer
ATTRIBUTION.txt neben der Ausgabe.
"""

from __future__ import annotations

import csv
from pathlib import Path

from .parse import Lead

OSM_ATTRIBUTION = "© OpenStreetMap-Mitwirkende (ODbL)"
GOOGLE_ATTRIBUTION = "Google Maps Platform (Places API)"

# Der OSM-Weg ist der Standard; Bestandscode und Tests beziehen sich darauf.
ATTRIBUTION = OSM_ATTRIBUTION

COLUMNS = (
    "name",
    "adresse",
    "strasse",
    "hausnummer",
    "plz",
    "ort",
    "telefon",
    "social",
    "kategorie",
    "quell_id",
    "quell_link",
    "maps_link",
    "quelle",
)

_OSM_NOTE = f"""Datenquelle: OpenStreetMap
Lizenz: Open Database License (ODbL) 1.0 — https://opendatacommons.org/licenses/odbl/
Pflichtangabe bei Weitergabe oder Veröffentlichung: {OSM_ATTRIBUTION}

Hinweis zur Aussagekraft: Ein fehlender `website`-Tag in OSM belegt nicht,
dass der Betrieb keine Webseite hat — er kann auch schlicht nicht erfasst
sein. Diese Liste ist eine Vorauswahl, keine geprüfte Menge.
"""

_GOOGLE_NOTE = f"""Datenquelle: {GOOGLE_ATTRIBUTION}

Nutzungsbedingungen: Die Google-Maps-Platform-Bedingungen beschränken das
Zwischenspeichern von Places-Inhalten (Richtwert 30 Tage) und untersagen den
Aufbau dauerhafter eigener Datenbanken. Dauerhaft gespeichert werden darf die
place_id (Spalte quell_id). Diese Liste ist deshalb zum Abarbeiten gedacht,
nicht zum Sammeln — nach der Kampagne löschen und bei Bedarf neu ziehen.

Hinweis zur Aussagekraft: Ein fehlendes Webseiten-Feld heißt, dass bei Google
keine Webseite hinterlegt ist. Der Betrieb kann trotzdem eine haben, die dort
nur nicht eingetragen ist.
"""

NOTES = {OSM_ATTRIBUTION: _OSM_NOTE, GOOGLE_ATTRIBUTION: _GOOGLE_NOTE}


def write_csv(
    leads: list[Lead],
    path: str | Path,
    delimiter: str = ";",
    quelle: str = ATTRIBUTION,
) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    with target.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=COLUMNS, delimiter=delimiter, extrasaction="ignore"
        )
        writer.writeheader()
        for lead in leads:
            writer.writerow(
                {
                    "name": lead.name,
                    "adresse": lead.adresse,
                    "strasse": lead.strasse,
                    "hausnummer": lead.hausnummer,
                    "plz": lead.plz,
                    "ort": lead.ort,
                    "telefon": lead.telefon,
                    "social": lead.social,
                    "kategorie": lead.kategorie,
                    "quell_id": lead.quell_id,
                    "quell_link": lead.quell_link,
                    "maps_link": lead.maps_link,
                    "quelle": quelle,
                }
            )

    (target.parent / "ATTRIBUTION.txt").write_text(
        NOTES.get(quelle, _OSM_NOTE), encoding="utf-8"
    )
    return target
