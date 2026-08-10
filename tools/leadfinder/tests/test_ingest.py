"""Der Regressionsschutz für den Fehler, der den Browser-Umweg lahmgelegt hat.

Die Anleitung im README verwies auf den GeoJSON-Export aus overpass-turbo, die
Verarbeitung las aber `elements`. Ergebnis: null Leads, keine Fehlermeldung —
nicht unterscheidbar von "es gibt in München nichts".
"""

import json
from pathlib import Path

import pytest

from leadfinder.ingest import UnknownFormat, normalize_payload
from leadfinder.parse import parse_elements

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def geojson() -> dict:
    return json.loads(
        (FIXTURES / "overpass_turbo_geojson.json").read_text(encoding="utf-8")
    )


@pytest.fixture
def overpass() -> dict:
    return json.loads(
        (FIXTURES / "overpass_muenchen.json").read_text(encoding="utf-8")
    )


def test_beide_formate_ergeben_dieselben_leads(geojson, overpass):
    """Der eigentliche Nachweis: vorher 6 gegen 0, jetzt 6 gegen 6."""
    aus_api, stats_api = parse_elements(normalize_payload(overpass))
    aus_browser, stats_browser = parse_elements(normalize_payload(geojson))

    assert [lead.name for lead in aus_api] == [lead.name for lead in aus_browser]
    assert stats_api.leads == stats_browser.leads == 6
    assert stats_api.duplikate == stats_browser.duplikate == 1
    assert stats_api.mit_webseite == stats_browser.mit_webseite == 1


def test_overpass_antwort_wird_durchgereicht(overpass):
    assert normalize_payload(overpass) is overpass["elements"]


def test_geojson_koordinaten_werden_gedreht(geojson):
    """GeoJSON schreibt [Länge, Breite] — genau andersherum als OSM sonst.

    Wer das verwechselt, landet mit München im Indischen Ozean, ohne dass
    irgendetwas abstürzt.
    """
    wagner = next(
        el for el in normalize_payload(geojson) if el["id"] == 1001
    )
    assert wagner["lat"] == pytest.approx(48.1371)
    assert wagner["lon"] == pytest.approx(11.5754)


def test_geojson_id_wird_in_typ_und_nummer_zerlegt(geojson):
    elements = normalize_payload(geojson)
    by_id = {(el["type"], el["id"]) for el in elements}
    assert ("node", 1001) in by_id
    assert ("way", 2002) in by_id
    assert ("relation", 9009) in by_id


def test_metafelder_landen_nicht_in_den_tags(geojson):
    """@id und @type sind Overpass-Metadaten, keine OSM-Tags.

    In den Tags würden sie die Kategorieerkennung stören.
    """
    for element in normalize_payload(geojson):
        assert not any(key.startswith("@") for key in element["tags"])


def test_polygon_bekommt_seinen_mittelpunkt(geojson):
    backhaus = next(el for el in normalize_payload(geojson) if el["id"] == 2002)
    assert backhaus["lat"] == pytest.approx(48.1503)
    assert backhaus["lon"] == pytest.approx(11.5808)


def test_unbekanntes_format_wird_laut_abgelehnt():
    """Still null zurückzugeben war genau der ursprüngliche Fehler."""
    with pytest.raises(UnknownFormat, match="weder 'elements'"):
        normalize_payload({"irgendwas": [1, 2, 3]})


def test_kein_objekt_wird_abgelehnt():
    with pytest.raises(UnknownFormat, match="list"):
        normalize_payload([{"type": "node"}])


def test_leere_sammlungen_sind_kein_fehler():
    assert normalize_payload({"elements": []}) == []
    assert normalize_payload({"features": []}) == []


def test_feature_ohne_geometrie_ueberlebt():
    elements = normalize_payload(
        {"features": [{"id": "node/1", "properties": {"name": "X"}}]}
    )
    assert elements[0]["tags"]["name"] == "X"
    assert "lat" not in elements[0]


def test_id_nur_in_properties_wird_gefunden():
    elements = normalize_payload(
        {"features": [{"properties": {"@id": "way/77", "name": "X"}}]}
    )
    assert elements[0]["type"] == "way"
    assert elements[0]["id"] == 77
