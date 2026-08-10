import pytest

from leadfinder.categories import (
    CATEGORIES,
    DEFAULT_CATEGORIES,
    in_gruppen,
    resolve,
    selector_index,
)


def test_kein_tagpaar_in_zwei_branchen():
    """Ein doppeltes Tag-Paar würde Treffer doppelt zählen.

    selector_index() nimmt beim Aufbau nur den ersten Treffer — die zweite
    Branche bekäme still gar nichts zugeordnet.
    """
    gesehen: dict[tuple[str, str], str] = {}
    doppelt = []
    for slug, cat in CATEGORIES.items():
        for selector in cat.selectors:
            if selector in gesehen:
                doppelt.append((selector, gesehen[selector], slug))
            gesehen[selector] = slug
    assert doppelt == []


def test_jede_branche_hat_selektoren_und_label():
    for slug, cat in CATEGORIES.items():
        assert cat.slug == slug
        assert cat.label.strip()
        assert cat.selectors


def test_selector_index_deckt_alle_paare_ab():
    index = selector_index()
    for cat in CATEGORIES.values():
        for selector in cat.selectors:
            assert selector in index


def test_standardbranchen_existieren():
    assert resolve(list(DEFAULT_CATEGORIES))


def test_tagschluessel_sind_die_ueblichen():
    """shop/craft/amenity/healthcare decken das Gewerbe in OSM ab.

    Ein Tippfehler im Schlüssel liefert keinen Fehler, sondern nichts —
    deshalb hier eine harte Grenze.
    """
    erlaubt = {"shop", "craft", "amenity", "healthcare", "office"}
    for cat in CATEGORIES.values():
        for key, _ in cat.selectors:
            assert key in erlaubt, f"{cat.slug}: unerwarteter Schlüssel {key}"


# --- Gruppierung -------------------------------------------------------------


def test_in_gruppen_teilt_vollstaendig_und_ohne_verlust():
    alle = list(CATEGORIES.values())
    gruppen = in_gruppen(alle, 4)
    assert [cat for gruppe in gruppen for cat in gruppe] == alle
    assert all(len(g) <= 4 for g in gruppen)


def test_in_gruppen_letzte_gruppe_darf_kleiner_sein():
    gruppen = in_gruppen(resolve(["friseur", "baeckerei", "kosmetik"]), 2)
    assert [len(g) for g in gruppen] == [2, 1]


def test_in_gruppen_eins_ergibt_je_eine_branche():
    alle = list(CATEGORIES.values())
    assert len(in_gruppen(alle, 1)) == len(alle)


def test_in_gruppen_lehnt_null_ab():
    with pytest.raises(ValueError):
        in_gruppen(list(CATEGORIES.values()), 0)
