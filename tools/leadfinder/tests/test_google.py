import json
from pathlib import Path

import pytest
import requests

from leadfinder import google as g
from leadfinder.budget import Budget
from leadfinder.categories import resolve

KEY = "AIza-GEHEIM-NICHT-LOGGEN"


@pytest.fixture
def pages() -> dict:
    path = Path(__file__).parent / "fixtures" / "google_places.json"
    return json.loads(path.read_text(encoding="utf-8"))


# --- Kachelung ---------------------------------------------------------------


def test_tiles_zerlegt_lueckenlos():
    tiles = g.tiles(g.MUENCHEN, grid=3)
    assert len(tiles) == 9
    assert min(t.sued for t in tiles) == pytest.approx(g.MUENCHEN.sued)
    assert max(t.nord for t in tiles) == pytest.approx(g.MUENCHEN.nord)
    assert min(t.west for t in tiles) == pytest.approx(g.MUENCHEN.west)
    assert max(t.ost for t in tiles) == pytest.approx(g.MUENCHEN.ost)


def test_tiles_grid_eins_ist_das_ganze_gebiet():
    assert g.tiles(g.MUENCHEN, grid=1) == [g.MUENCHEN]


def test_tiles_lehnt_unsinn_ab():
    with pytest.raises(ValueError):
        g.tiles(g.MUENCHEN, grid=0)


def test_estimate_waechst_quadratisch_mit_dem_raster():
    assert g.estimate_requests(2, 3, 1) == 18
    assert g.estimate_requests(2, 6, 1) == 72


# --- Request-Aufbau ----------------------------------------------------------


def test_body_setzt_gebietsbeschraenkung_und_sprache():
    body = g.build_body("Friseur", g.MUENCHEN)
    rect = body["locationRestriction"]["rectangle"]
    assert rect["low"]["latitude"] == g.MUENCHEN.sued
    assert rect["high"]["longitude"] == g.MUENCHEN.ost
    assert body["languageCode"] == "de"
    assert body["regionCode"] == "DE"
    assert "pageToken" not in body


def test_body_reicht_pagetoken_durch():
    assert g.build_body("Friseur", g.MUENCHEN, "TOKEN")["pageToken"] == "TOKEN"


def test_feldmaske_enthaelt_die_entscheidenden_felder():
    """websiteUri trägt den ganzen Filter, addressComponents die Adresse.

    Fehlt websiteUri, filtert das Tool nichts mehr und liefert alle Betriebe.
    """
    assert "places.websiteUri" in g.FIELD_MASK
    assert "places.addressComponents" in g.FIELD_MASK
    assert "places.nationalPhoneNumber" in g.FIELD_MASK
    assert "nextPageToken" in g.FIELD_MASK


def test_key_geht_in_den_header_nicht_in_die_url(monkeypatch):
    """URLs landen in Proxy- und Serverlogs, Header deutlich seltener."""
    gesehen = {}

    def fake_post(url, **kwargs):
        gesehen["url"] = url
        gesehen["headers"] = kwargs.get("headers", {})
        return type("R", (), {"status_code": 200, "ok": True, "text": "",
                              "json": lambda self: {"places": []}})()

    monkeypatch.setattr(g.requests, "post", fake_post)
    g.search_page("Friseur", g.MUENCHEN, KEY)

    assert gesehen["headers"]["X-Goog-Api-Key"] == KEY
    assert KEY not in gesehen["url"]
    assert gesehen["headers"]["X-Goog-FieldMask"] == g.FIELD_MASK


# --- Fehler und Key-Schutz ---------------------------------------------------


def test_scrub_entfernt_den_key():
    assert KEY not in g.scrub(f"Fehler bei key={KEY} aufgetreten", KEY)


def test_authfehler_verraet_den_key_nicht(monkeypatch):
    """Fehlermeldungen wandern in Logs und Bugreports.

    Ein Key, der dort einmal steht, ist verbrannt.
    """
    monkeypatch.setattr(
        g.requests,
        "post",
        lambda url, **kw: type(
            "R",
            (),
            {
                "status_code": 403,
                "ok": False,
                "text": f"PERMISSION_DENIED for key {KEY}",
                "json": lambda self: {},
            },
        )(),
    )
    with pytest.raises(g.GoogleAuthError) as exc:
        g.search_page("Friseur", g.MUENCHEN, KEY)
    assert KEY not in str(exc.value)
    assert "***" in str(exc.value)


def test_netzfehler_wird_als_unreachable_gemeldet(monkeypatch):
    monkeypatch.setattr(
        g.requests,
        "post",
        lambda url, **kw: (_ for _ in ()).throw(requests.ConnectionError()),
    )
    with pytest.raises(g.GoogleUnreachable):
        g.search_page("Friseur", g.MUENCHEN, KEY)


def test_serverfehler_ist_kein_netzfehler(monkeypatch):
    monkeypatch.setattr(
        g.requests,
        "post",
        lambda url, **kw: type(
            "R",
            (),
            {"status_code": 500, "ok": False, "text": "boom",
             "json": lambda self: {}},
        )(),
    )
    with pytest.raises(g.GoogleError, match="500"):
        g.search_page("Friseur", g.MUENCHEN, KEY)


# --- Abbildung ---------------------------------------------------------------


def test_place_to_lead_zerlegt_die_adresse(pages):
    place = pages["page1"]["places"][0]
    lead = g.place_to_lead(place, "Friseur")

    assert lead.name == "Friseursalon Wagner"
    assert lead.strasse == "Sendlinger Straße"
    assert lead.hausnummer == "12"
    assert lead.plz == "80331"
    assert lead.ort == "München"
    assert lead.telefon == "+498912345678"
    assert lead.quell_id == "ChIJAAAAAAAAAAARwagner00001"
    assert "place_id:ChIJAAAAAAAAAAARwagner00001" in lead.quell_link


def test_place_to_lead_ohne_namen_ist_kein_lead(pages):
    ohne_name = pages["page1"]["places"][3]
    assert g.place_to_lead(ohne_name, "Friseur") is None


def test_has_website(pages):
    assert g.has_website(pages["page1"]["places"][1]) is True
    assert g.has_website(pages["page1"]["places"][0]) is False


# --- Zusammenspiel -----------------------------------------------------------


def _stub(pages, calls=None):
    def search(text_query, tile, api_key, page_token=None, timeout=30.0):
        if calls is not None:
            calls.append(page_token)
        return pages["page2"] if page_token else pages["page1"]

    return search


def test_collect_paginiert_filtert_und_dedupliziert(tmp_path, pages):
    budget = Budget(limit=100, path=tmp_path / "b.json")
    leads, stats = g.collect(
        resolve(["friseur"]),
        KEY,
        budget,
        grid=1,
        max_pages=2,
        search=_stub(pages),
    )

    namen = [lead.name for lead in leads]
    assert namen == ["Friseursalon Wagner", "Backhaus Sonnenschein"]
    assert stats.mit_webseite == 1      # Coiffeur MitWebseite
    assert stats.ohne_telefon == 1      # Haarstudio Ohne Telefon
    assert stats.ohne_name == 1         # Eintrag ohne displayName
    assert stats.duplikate == 1         # Wagner steht auf beiden Seiten
    assert stats.adresse_unvollstaendig == 1  # Backhaus ohne Hausnummer
    assert stats.leads == 2


def test_collect_folgt_nextpagetoken(tmp_path, pages):
    calls: list = []
    g.collect(
        resolve(["friseur"]),
        KEY,
        Budget(limit=100, path=tmp_path / "b.json"),
        grid=1,
        max_pages=2,
        search=_stub(pages, calls),
    )
    assert calls == [None, "TOKEN-SEITE-2"]


def test_collect_stoppt_an_der_budgetgrenze(tmp_path, pages):
    """An der Grenze abbrechen, aber die bisherigen Leads behalten.

    Alles wegzuwerfen hieße: bezahlt und nichts bekommen.
    """
    budget = Budget(limit=1, path=tmp_path / "b.json")
    leads, stats = g.collect(
        resolve(["friseur", "baeckerei"]),
        KEY,
        budget,
        grid=2,
        max_pages=1,
        search=_stub(pages),
    )
    assert budget.used == 1
    assert len(leads) >= 1
    assert stats.leads == len(leads)


def test_collect_zaehlt_jede_abfrage(tmp_path, pages):
    budget = Budget(limit=100, path=tmp_path / "b.json")
    g.collect(
        resolve(["friseur"]),
        KEY,
        budget,
        grid=2,
        max_pages=1,
        search=_stub(pages),
    )
    assert budget.used == 4  # 1 Branche x 4 Kacheln


def test_collect_ohne_telefonpflicht_nimmt_mehr_auf(tmp_path, pages):
    streng, _ = g.collect(
        resolve(["friseur"]), KEY, Budget(limit=100, path=tmp_path / "a.json"),
        grid=1, max_pages=2, search=_stub(pages),
    )
    locker, _ = g.collect(
        resolve(["friseur"]), KEY, Budget(limit=100, path=tmp_path / "b.json"),
        grid=1, max_pages=2, require_phone=False, search=_stub(pages),
    )
    assert len(locker) == len(streng) + 1
