"""CSV-Ausgabe.

Zwei Entscheidungen sind auf deutsches Excel gemünzt: Semikolon als Trenner
und UTF-8 *mit* BOM. Ohne BOM zeigt Excel "Bäckerei" als "BÃ¤ckerei" — die
Datei wäre technisch korrekt und praktisch unbrauchbar.

Die ODbL verlangt Namensnennung bei Weitergabe der Daten. Statt einer
Kommentarzeile, die jeden CSV-Parser stört, trägt jede Zeile eine Spalte
`quelle`; zusätzlich wird eine ATTRIBUTION.txt neben die Ausgabe gelegt.
"""

from __future__ import annotations

import csv
from pathlib import Path

from .parse import Lead

ATTRIBUTION = "© OpenStreetMap-Mitwirkende (ODbL)"

COLUMNS = (
    "name",
    "adresse",
    "strasse",
    "hausnummer",
    "plz",
    "ort",
    "telefon",
    "kategorie",
    "osm_id",
    "osm_link",
    "maps_link",
    "quelle",
)

ATTRIBUTION_NOTE = f"""Datenquelle: OpenStreetMap
Lizenz: Open Database License (ODbL) 1.0 — https://opendatacommons.org/licenses/odbl/
Pflichtangabe bei Weitergabe oder Veröffentlichung: {ATTRIBUTION}

Hinweis zur Aussagekraft: Ein fehlender `website`-Tag in OSM belegt nicht,
dass der Betrieb keine Webseite hat — er kann auch schlicht nicht erfasst
sein. Diese Liste ist eine Vorauswahl, keine geprüfte Menge.
"""


def write_csv(
    leads: list[Lead],
    path: str | Path,
    delimiter: str = ";",
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
                    "kategorie": lead.kategorie,
                    "osm_id": lead.osm_id,
                    "osm_link": lead.osm_link,
                    "maps_link": lead.maps_link,
                    "quelle": ATTRIBUTION,
                }
            )

    (target.parent / "ATTRIBUTION.txt").write_text(
        ATTRIBUTION_NOTE, encoding="utf-8"
    )
    return target
