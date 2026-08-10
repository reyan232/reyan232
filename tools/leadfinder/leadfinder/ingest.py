"""Gespeicherte Antworten einlesen, egal in welchem Format sie vorliegen.

Overpass liefert je nach Ausgabeweg zwei völlig verschiedene Strukturen: die
API selbst gibt `{"elements": [...]}`, der Export aus overpass-turbo gibt
GeoJSON mit `{"features": [...]}`. Wer aus dem Browser exportiert, bekommt
fast immer das zweite.

Das nur für eine Form auszulegen ist heimtückisch: `payload.get("elements")`
liefert bei GeoJSON schlicht eine leere Liste, der Lauf endet mit null Leads
und ohne Fehler — das sieht aus wie "in München gibt es nichts" statt nach
"falsches Format". Deshalb hier beides annehmen und alles andere laut ablehnen.
"""

from __future__ import annotations

# In overpass-turbo-Exporten stehen neben den echten Tags auch Metafelder mit
# @-Präfix (@id, @type, @timestamp). Die sind keine OSM-Tags und würden sonst
# in der Kategorieerkennung landen.
_META_PREFIX = "@"


class UnknownFormat(ValueError):
    """Datei ist JSON, aber weder Overpass-Antwort noch GeoJSON."""


def normalize_payload(data: object) -> list[dict]:
    """Beliebige gespeicherte Antwort zu Overpass-Elementen normalisieren."""
    if not isinstance(data, dict):
        raise UnknownFormat(
            "Erwartet wird ein JSON-Objekt, gefunden wurde "
            f"{type(data).__name__}."
        )

    if isinstance(data.get("elements"), list):
        return data["elements"]

    if isinstance(data.get("features"), list):
        return [_feature_to_element(f) for f in data["features"]]

    raise UnknownFormat(
        "Unbekanntes Format: weder 'elements' (Overpass-API-Antwort) noch "
        "'features' (GeoJSON) gefunden.\n"
        "Aus overpass-turbo funktionieren beide Exportwege — "
        "'GeoJSON' ebenso wie 'raw data directly from Overpass API'."
    )


def _split_id(raw: object) -> tuple[str, object]:
    """'node/1001' zu ('node', 1001) auflösen.

    GeoJSON-Features tragen die OSM-Identität als zusammengesetzte
    Zeichenkette; für die Deduplizierung brauchen wir Typ und Nummer getrennt.
    """
    text = str(raw or "")
    if "/" in text:
        kind, _, number = text.partition("/")
        return kind, int(number) if number.isdigit() else number
    return "node", text


def _coords_from_geometry(geometry: dict | None) -> tuple[float | None, float | None]:
    """Mittelpunkt einer Geometrie als (lat, lon).

    GeoJSON schreibt Koordinaten als [Länge, Breite] — genau andersherum als
    die restliche OSM-Welt. Wer das verwechselt, landet mit München im Indischen
    Ozean, ohne dass irgendetwas abstürzt.
    """
    if not geometry:
        return None, None

    coordinates = geometry.get("coordinates")
    if coordinates is None:
        return None, None

    points = list(_flatten_points(coordinates))
    if not points:
        return None, None

    lons = [p[0] for p in points]
    lats = [p[1] for p in points]
    return (min(lats) + max(lats)) / 2, (min(lons) + max(lons)) / 2


def _flatten_points(node: object):
    """Punktpaare aus beliebig verschachtelten Koordinatenlisten holen."""
    if (
        isinstance(node, (list, tuple))
        and len(node) >= 2
        and all(isinstance(v, (int, float)) for v in node[:2])
    ):
        yield float(node[0]), float(node[1])
        return
    if isinstance(node, (list, tuple)):
        for child in node:
            yield from _flatten_points(child)


def _feature_to_element(feature: dict) -> dict:
    properties = feature.get("properties") or {}
    tags = {
        key: value
        for key, value in properties.items()
        if not key.startswith(_META_PREFIX)
    }

    # Die Identität steht mal oben am Feature, mal als @id in den Properties.
    raw_id = feature.get("id") or properties.get("@id") or ""
    kind, number = _split_id(raw_id)
    if properties.get("@type"):
        kind = properties["@type"]

    lat, lon = _coords_from_geometry(feature.get("geometry"))

    element: dict = {"type": kind, "id": number, "tags": tags}
    if lat is not None and lon is not None:
        element["lat"] = lat
        element["lon"] = lon
    return element
