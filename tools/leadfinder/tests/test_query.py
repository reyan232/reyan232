import pytest

from leadfinder.categories import CATEGORIES, resolve
from leadfinder.query import build_query


def test_resolve_meldet_tippfehler_sofort():
    """Ein Tippfehler soll scheitern, nicht als leeres Ergebnis auffallen."""
    with pytest.raises(ValueError, match="friso"):
        resolve(["friso"])


def test_resolve_liefert_kategorien():
    assert [c.slug for c in resolve(["friseur", "gastro"])] == ["friseur", "gastro"]


def test_build_query_grundgeruest():
    query = build_query(resolve(["friseur"]))
    assert "[out:json][timeout:180];" in query
    assert '"name"="München"' in query
    assert '"admin_level"="6"' in query
    assert 'nwr["shop"="hairdresser"]' in query
    assert query.rstrip().endswith("out center tags;")


def test_build_query_schliesst_alle_webseiten_tags_aus():
    query = build_query(resolve(["friseur"]))
    for tag in ("website", "contact:website", "url"):
        assert f'[!"{tag}"]' in query


def test_build_query_eine_klausel_je_tagpaar():
    gastro = CATEGORIES["gastro"]
    query = build_query([gastro])
    assert query.count("nwr[") == len(gastro.selectors)


def test_build_query_ohne_kategorie_ist_fehler():
    with pytest.raises(ValueError, match="Keine Branche"):
        build_query([])


@pytest.mark.parametrize(
    "area",
    ['München"]; out count; //', "Bad\\Name", "x[!website]", "a;b"],
)
def test_build_query_weist_gefaehrliche_gebietsnamen_ab(area):
    """Der Gebietsname landet unescaped in der Abfrage.

    Statt zu escapen lassen wir nur harmlose Zeichen zu — ein Name braucht
    nicht mehr, und so kann keine Eingabe die Abfrage umschreiben.
    """
    with pytest.raises(ValueError, match="Unzulässige Zeichen"):
        build_query(resolve(["friseur"]), area_name=area)


def test_build_query_erlaubt_echte_ortsnamen():
    for area in ["München", "Bad Tölz", "Garmisch-Partenkirchen", "Sankt Ottilien"]:
        assert area in build_query(resolve(["friseur"]), area_name=area)
