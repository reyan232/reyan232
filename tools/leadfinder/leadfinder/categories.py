"""Branchen als OSM-Tag-Selektoren.

OSM kennt keine "Branche", sondern Tag-Paare wie ``shop=hairdresser``. Eine
Branche im Vertriebssinn ist deshalb eine Menge solcher Paare — Gastronomie
umfasst Restaurant, Café, Bar und Imbiss, die in OSM vier getrennte Werte sind.

Die Auswahl hier ist bewusst klein (Testlauf). Erweitern heißt: Eintrag
ergänzen. Werte gegen das OSM-Wiki prüfen, sonst liefert die Abfrage still
nichts — ein falscher Tag-Wert ist kein Fehler, nur eine leere Menge.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
    slug: str
    label: str
    selectors: tuple[tuple[str, str], ...]


CATEGORIES: dict[str, Category] = {
    "friseur": Category(
        "friseur",
        "Friseur",
        (("shop", "hairdresser"),),
    ),
    "baeckerei": Category(
        "baeckerei",
        "Bäckerei",
        (("shop", "bakery"), ("shop", "pastry")),
    ),
    "kosmetik": Category(
        "kosmetik",
        "Kosmetik",
        (("shop", "beauty"), ("shop", "cosmetics"), ("shop", "nail_salon")),
    ),
    "handwerk": Category(
        "handwerk",
        "Handwerk",
        (
            ("craft", "plumber"),
            ("craft", "electrician"),
            ("craft", "painter"),
            ("craft", "carpenter"),
            ("craft", "roofer"),
            ("craft", "tiler"),
        ),
    ),
    "gastro": Category(
        "gastro",
        "Gastronomie",
        (
            ("amenity", "restaurant"),
            ("amenity", "cafe"),
            ("amenity", "bar"),
            ("amenity", "fast_food"),
        ),
    ),
    "metzger": Category("metzger", "Metzgerei", (("shop", "butcher"),)),
    "blumen": Category("blumen", "Blumen", (("shop", "florist"),)),
    "optiker": Category("optiker", "Optiker", (("shop", "optician"),)),
    "schneiderei": Category(
        "schneiderei",
        "Schneiderei",
        (("craft", "tailor"), ("shop", "tailor")),
    ),
    "autowerkstatt": Category(
        "autowerkstatt", "Autowerkstatt", (("shop", "car_repair"),)
    ),
    "reinigung": Category(
        "reinigung",
        "Reinigung",
        (("shop", "dry_cleaning"), ("shop", "laundry")),
    ),
    "schuster": Category(
        "schuster",
        "Schuster",
        (("craft", "shoemaker"), ("shop", "shoe_repair")),
    ),
    "fahrschule": Category(
        "fahrschule", "Fahrschule", (("amenity", "driving_school"),)
    ),
    "tierarzt": Category("tierarzt", "Tierarzt", (("amenity", "veterinary"),)),
    "reisebuero": Category(
        "reisebuero", "Reisebüro", (("shop", "travel_agency"),)
    ),
}

DEFAULT_CATEGORIES = ("friseur", "baeckerei", "kosmetik")


def resolve(slugs: list[str] | tuple[str, ...]) -> list[Category]:
    """Slugs zu Kategorien auflösen; unbekannte Slugs sofort melden.

    Ein Tippfehler soll hier scheitern und nicht erst als leeres Ergebnis
    auffallen, wenn die Abfrage längst gelaufen ist.
    """
    unknown = [s for s in slugs if s not in CATEGORIES]
    if unknown:
        raise ValueError(
            f"Unbekannte Branche(n): {', '.join(unknown)}. "
            f"Verfügbar: {', '.join(sorted(CATEGORIES))}"
        )
    return [CATEGORIES[s] for s in slugs]


def selector_index() -> dict[tuple[str, str], Category]:
    """Rückwärts-Zuordnung Tag-Paar -> Kategorie, für die Auswertung.

    Ein Element kann mehrere passende Tags tragen; die Zuordnung nimmt das
    erste Treffer-Paar, was für die Spalte "kategorie" ausreicht.
    """
    index: dict[tuple[str, str], Category] = {}
    for cat in CATEGORIES.values():
        for sel in cat.selectors:
            index.setdefault(sel, cat)
    return index


def in_gruppen(categories: list[Category], groesse: int) -> list[list[Category]]:
    """Branchen in Blöcke teilen — für getrennte Abfragen und Links.

    Nötig aus zwei Richtungen: eine URL mit allen Branchen wird zu lang, und
    eine Overpass-Abfrage über ganz München mit dutzenden Selektoren läuft in
    den Timeout. Kleine Blöcke lösen beides und sind gegenüber einem
    Spendendienst auch das anständigere Verhalten.
    """
    if groesse < 1:
        raise ValueError("Gruppengröße muss mindestens 1 sein")
    return [
        categories[i : i + groesse] for i in range(0, len(categories), groesse)
    ]
