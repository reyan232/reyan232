"""Netzwerkverhalten ohne Netzwerk prüfen.

Overpass ist ein Spendendienst; ob wir uns höflich verhalten (Backoff statt
Nachbohren, Spiegelwechsel erst nach Fehlschlag) lässt sich nur hier belegen,
weil es im Echtlauf niemand sieht.
"""

import pytest
import requests

from leadfinder import fetch as fetch_mod
from leadfinder.fetch import (
    OverpassError,
    OverpassUnreachable,
    check_reachability,
    fetch,
)

MIRRORS = ("https://m1.test/api/interpreter", "https://m2.test/api/interpreter")


class FakeResponse:
    def __init__(self, status_code=200, payload=None, text="", json_error=False):
        self.status_code = status_code
        self._payload = payload if payload is not None else {"elements": []}
        self.text = text
        self._json_error = json_error

    @property
    def ok(self):
        return 200 <= self.status_code < 300

    def json(self):
        if self._json_error:
            raise ValueError("keine gültige JSON-Antwort")
        return self._payload


def test_fetch_erfolg_beim_ersten_spiegel(monkeypatch):
    calls = []

    def fake_post(url, **kwargs):
        calls.append(url)
        return FakeResponse(payload={"elements": [{"id": 1}]})

    monkeypatch.setattr(fetch_mod.requests, "post", fake_post)
    result = fetch("query", mirrors=MIRRORS, sleep=lambda _: None)

    assert result == {"elements": [{"id": 1}]}
    assert calls == [MIRRORS[0]]


def test_fetch_wartet_bei_ueberlast_und_versucht_erneut(monkeypatch):
    responses = [FakeResponse(429), FakeResponse(504), FakeResponse(payload={"ok": 1})]
    waits = []

    monkeypatch.setattr(
        fetch_mod.requests, "post", lambda url, **kw: responses.pop(0)
    )
    result = fetch("q", mirrors=MIRRORS, sleep=waits.append)

    assert result == {"ok": 1}
    # Backoff muss wachsen, sonst ist es kein Backoff.
    assert waits == [2, 4]


def test_fetch_wechselt_bei_netzfehler_den_spiegel(monkeypatch):
    calls = []

    def fake_post(url, **kwargs):
        calls.append(url)
        if url == MIRRORS[0]:
            raise requests.ConnectionError("kein Weg raus")
        return FakeResponse(payload={"ok": 2})

    monkeypatch.setattr(fetch_mod.requests, "post", fake_post)
    assert fetch("q", mirrors=MIRRORS, sleep=lambda _: None) == {"ok": 2}
    # Bei Netzfehler nicht wiederholen, sondern weiterziehen.
    assert calls == [MIRRORS[0], MIRRORS[1]]


def test_fetch_alle_spiegel_tot_ergibt_unreachable(monkeypatch):
    def fake_post(url, **kwargs):
        raise requests.ConnectionError("blockiert")

    monkeypatch.setattr(fetch_mod.requests, "post", fake_post)
    with pytest.raises(OverpassUnreachable, match="Kein Overpass-Spiegel erreichbar"):
        fetch("q", mirrors=MIRRORS, sleep=lambda _: None)


def test_fetch_abgelehnte_abfrage_ist_kein_netzproblem(monkeypatch):
    monkeypatch.setattr(
        fetch_mod.requests,
        "post",
        lambda url, **kw: FakeResponse(400, text="Syntaxfehler in Zeile 3"),
    )
    with pytest.raises(OverpassError, match="Syntaxfehler"):
        fetch("q", mirrors=MIRRORS, sleep=lambda _: None)


def test_fetch_kaputtes_json_wird_klar_gemeldet(monkeypatch):
    monkeypatch.setattr(
        fetch_mod.requests, "post", lambda url, **kw: FakeResponse(json_error=True)
    )
    with pytest.raises(OverpassError, match="kein JSON"):
        fetch("q", mirrors=MIRRORS, sleep=lambda _: None)


def test_fetch_sendet_user_agent(monkeypatch):
    seen = {}

    def fake_post(url, **kwargs):
        seen.update(kwargs.get("headers", {}))
        return FakeResponse()

    monkeypatch.setattr(fetch_mod.requests, "post", fake_post)
    fetch("q", mirrors=MIRRORS, user_agent="leadfinder-test/1.0", sleep=lambda _: None)
    assert seen["User-Agent"] == "leadfinder-test/1.0"


def test_check_reachability_unterscheidet_blockiert_und_fehler(monkeypatch):
    def fake_get(url, **kwargs):
        if "m1" in url:
            raise requests.ConnectionError("blockiert")
        return FakeResponse(503)

    monkeypatch.setattr(fetch_mod.requests, "get", fake_get)
    results = check_reachability(MIRRORS)

    assert results[0][1] == "blockiert"
    assert results[1][1] == "HTTP 503"


def test_check_reachability_fragt_status_endpunkt(monkeypatch):
    urls = []
    monkeypatch.setattr(
        fetch_mod.requests,
        "get",
        lambda url, **kw: urls.append(url) or FakeResponse(),
    )
    check_reachability(MIRRORS)
    assert all(url.endswith("/api/status") for url in urls)
