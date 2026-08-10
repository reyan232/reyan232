"""Overpass-QL-Abfragen bauen.

Der Webseiten-Ausschluss passiert serverseitig: Betriebe *mit* Webseite sollen
gar nicht erst übertragen werden. Der Telefonfilter dagegen läuft lokal
(siehe parse.py), weil die Quote "wie viele Treffer haben keine Nummer" die
entscheidende Kennzahl für die Datenqualität ist — serverseitig gefiltert
wüssten wir sie nicht.
"""

from __future__ import annotations

import re
from urllib.parse import quote

from .categories import Category

TURBO_BASE = "https://overpass-turbo.eu/"

# Tags, deren Vorhandensein "hat eine Webseite" bedeutet. `url` ist selten und
# uneinheitlich benutzt, schließt aber zuverlässig genug aus.
WEBSITE_TAGS = ("website", "contact:website", "url")

# Overpass-Werte werden in Anführungszeichen eingesetzt. Statt zu escapen
# lassen wir nur unkritische Zeichen zu — Gebietsnamen brauchen nicht mehr,
# und so kann kein Eingabewert die Abfrage umschreiben.
_SAFE_VALUE = re.compile(r"^[\w\s.'\-/()äöüÄÖÜß]+$", re.UNICODE)


def _check(value: str, what: str) -> str:
    if not _SAFE_VALUE.match(value):
        raise ValueError(f"Unzulässige Zeichen in {what}: {value!r}")
    return value


# Overpass adressiert Flächen als Relations-ID plus diesem Versatz.
AREA_OFFSET = 3600000000


def build_query(
    categories: list[Category],
    area_name: str = "München",
    timeout: int = 180,
    admin_level: str = "6",
    area_id: int | None = None,
) -> str:
    """Overpass QL für die gegebenen Branchen im gegebenen Gebiet.

    Standardmäßig wird das Gebiet über den Namen aufgelöst — selbsterklärend
    und ohne Netzzugang prüfbar. Der Haken: trägt eine zweite Fläche derselben
    Verwaltungsstufe denselben Namen (etwa Stadt und Landkreis München), dann
    vereinigt Overpass beide, und in den Ergebnissen stehen Betriebe aus dem
    Umland — ohne jede Fehlermeldung.

    `area_id` pinnt die Fläche deshalb auf eine bestimmte OSM-Relation und
    macht das Ergebnis eindeutig. Hier ist keine ID fest verdrahtet: sie ließe
    sich in dieser Umgebung nicht verifizieren, und eine falsch geratene ID
    wäre schlimmer als der Namensweg.
    """
    if not categories:
        raise ValueError("Keine Branche ausgewählt.")
    _check(admin_level, "admin_level")

    if area_id is not None:
        if area_id <= 0:
            raise ValueError("area_id muss eine positive Relations-ID sein")
        area_line = f"area({AREA_OFFSET + int(area_id)})->.a;"
    else:
        _check(area_name, "Gebietsname")
        area_line = (
            f'area["name"="{area_name}"]["boundary"="administrative"]'
            f'["admin_level"="{admin_level}"]->.a;'
        )

    exclude = "".join(f'[!"{tag}"]' for tag in WEBSITE_TAGS)

    clauses: list[str] = []
    for cat in categories:
        for key, value in cat.selectors:
            _check(key, "Tag-Schlüssel")
            _check(value, "Tag-Wert")
            clauses.append(f'  nwr["{key}"="{value}"]{exclude}(area.a);')

    body = "\n".join(clauses)
    return (
        f"[out:json][timeout:{int(timeout)}];\n"
        f"{area_line}\n"
        f"(\n{body}\n);\n"
        f"out center tags;\n"
    )


def turbo_url(query: str, run: bool = True) -> str:
    """Abfrage als anklickbaren overpass-turbo-Link verpacken.

    Der Umweg über den Browser ist für jeden gedacht, dessen Netz Overpass
    sperrt oder der kein Python installieren will: Link öffnen, Ergebnis
    exportieren, Datei mit --from-file auswerten.

    `safe=""` ist wichtig — Zeichen wie `/`, `[`, `]` und `;` sind Teil der
    Abfrage und dürfen nicht als URL-Syntax durchrutschen.
    """
    url = f"{TURBO_BASE}?Q={quote(query, safe='')}"
    return url + "&R" if run else url
