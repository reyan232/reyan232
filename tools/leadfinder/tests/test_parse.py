import pytest

from leadfinder.parse import (
    build_address,
    element_to_lead,
    has_website,
    normalize_phone,
    parse_elements,
    pick_phone,
)


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("089/123 456 78", "+498912345678"),
        ("+49 89 99 98 88", "+4989999888"),
        ("004989123450", "+4989123450"),
        ("0176 12345678", "+4917612345678"),
        ("(089) 12-34-56", "+4989123456"),
        ("089.123456", "+4989123456"),
        # Mehrere Nummern: die erste zählt, der Rest wird verworfen.
        ("089/111 222; 089/333 444", "+4989111222"),
    ],
)
def test_normalize_phone_deutsche_schreibweisen(raw, expected):
    assert normalize_phone(raw) == expected


@pytest.mark.parametrize("raw", ["", "   ", "12345", "abc", "0", "0123"])
def test_normalize_phone_gibt_none_statt_zu_raten(raw):
    """Ohne führende 0/+/00 ist die Vorwahl unbekannt.

    Raten würde falsche Nummern erzeugen, und eine falsche Nummer kostet im
    Vertrieb mehr als eine fehlende.
    """
    assert normalize_phone(raw) is None


def test_pick_phone_behaelt_rohwert_wenn_nicht_normierbar():
    number, normalized = pick_phone({"phone": "12345"})
    assert number == "12345"
    assert normalized is False


def test_pick_phone_nutzt_contact_praefix():
    assert pick_phone({"contact:phone": "089/1 22 33"})[0] == "+498912233"


def test_pick_phone_ohne_nummer():
    assert pick_phone({"name": "X"}) == ("", True)


def test_build_address_vollstaendig():
    address, complete = build_address(
        {
            "addr:street": "Sendlinger Straße",
            "addr:housenumber": "12",
            "addr:postcode": "80331",
            "addr:city": "München",
        }
    )
    assert address == "Sendlinger Straße 12, 80331 München"
    assert complete is True


def test_build_address_lueckenhaft_bleibt_lesbar():
    address, complete = build_address(
        {"addr:street": "Leopoldstraße", "addr:city": "München"}
    )
    assert address == "Leopoldstraße, München"
    assert complete is False


def test_build_address_leer():
    assert build_address({}) == ("", False)


@pytest.mark.parametrize(
    "tags,expected",
    [
        ({"website": "https://x.de"}, True),
        ({"contact:website": "https://x.de"}, True),
        ({"url": "https://x.de"}, True),
        ({"website": "   "}, False),
        ({"name": "X"}, False),
    ],
)
def test_has_website(tags, expected):
    assert has_website(tags) is expected


def test_element_to_lead_way_nutzt_center_koordinaten():
    lead = element_to_lead(
        {
            "type": "way",
            "id": 42,
            "center": {"lat": 48.15, "lon": 11.58},
            "tags": {"shop": "bakery", "name": "Testbäckerei"},
        }
    )
    assert lead.lat == 48.15 and lead.lon == 11.58
    assert lead.osm_id == "way/42"
    assert lead.osm_link == "https://www.openstreetmap.org/way/42"
    assert "48.15,11.58" in lead.maps_link


def test_element_to_lead_ohne_namen_ist_kein_lead():
    assert element_to_lead({"type": "node", "id": 1, "tags": {"shop": "bakery"}}) is None


def test_parse_elements_kennzahlen(elements):
    leads, stats = parse_elements(elements)

    assert stats.elemente == 10
    assert stats.ohne_name == 1
    assert stats.ohne_telefon == 1
    assert stats.telefon_unparsbar == 1
    assert stats.adresse_unvollstaendig == 1
    assert stats.duplikate == 1
    assert stats.mit_webseite == 1
    assert stats.leads == 6
    assert len(leads) == 6


def test_parse_elements_dedupliziert_ueber_osm_id(elements):
    leads, _ = parse_elements(elements)
    ids = [lead.osm_id for lead in leads]
    assert len(ids) == len(set(ids))
    assert ids.count("node/1001") == 1


def test_parse_elements_filtert_webseiten_betriebe_heraus(elements):
    leads, _ = parse_elements(elements)
    assert all("MitWebseite" not in lead.name for lead in leads)


def test_parse_elements_ohne_telefonpflicht_nimmt_mehr_auf(elements):
    strict, _ = parse_elements(elements, require_phone=True)
    loose, _ = parse_elements(elements, require_phone=False)
    assert len(loose) == len(strict) + 1
    assert any(lead.telefon == "" for lead in loose)


def test_parse_elements_kategorien(elements):
    _, stats = parse_elements(elements)
    assert stats.kategorien == {
        "Friseur": 1,
        "Bäckerei": 2,
        "Handwerk": 1,
        "Gastronomie": 2,
    }


def test_stats_zeilen_sind_lesbar(elements):
    _, stats = parse_elements(elements)
    text = "\n".join(stats.as_lines())
    assert "brauchbare Leads" in text
    assert "je Branche" in text
