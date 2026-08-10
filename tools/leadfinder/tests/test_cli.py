import csv

import requests

from leadfinder import fetch as fetch_mod
from leadfinder.cli import EXIT_ERROR, EXIT_OK, EXIT_UNREACHABLE, main


def test_list_categories(capsys):
    assert main(["--list-categories"]) == EXIT_OK
    out = capsys.readouterr().out
    assert "friseur" in out and "shop=hairdresser" in out


def test_dry_run_zeigt_abfrage_ohne_netz(capsys, monkeypatch):
    def explode(*args, **kwargs):
        raise AssertionError("dry-run darf nichts senden")

    monkeypatch.setattr(fetch_mod.requests, "post", explode)
    assert main(["--dry-run", "--categories", "friseur"]) == EXIT_OK

    out = capsys.readouterr().out
    assert 'nwr["shop"="hairdresser"]' in out
    assert "out center tags;" in out


def test_unbekannte_branche_ist_fehler(capsys):
    assert main(["--categories", "quatsch"]) == EXIT_ERROR
    assert "Unbekannte Branche" in capsys.readouterr().err


def test_self_check_meldet_blockade_mit_eigenem_exitcode(capsys, monkeypatch):
    """In gesperrten Netzen ist das die häufigste Situation.

    Sie muss als Netzsperre erkennbar sein und nicht wie ein Datenproblem
    aussehen — deshalb ein eigener Exit-Code und ein Klartexthinweis.
    """
    monkeypatch.setattr(
        fetch_mod.requests,
        "get",
        lambda url, **kw: (_ for _ in ()).throw(requests.ConnectionError()),
    )
    assert main(["--self-check"]) == EXIT_UNREACHABLE
    out = capsys.readouterr().out
    assert "Kein Spiegel erreichbar" in out
    assert "Netzsperre" in out


def test_self_check_ok(capsys, monkeypatch):
    class R:
        ok = True
        status_code = 200

    monkeypatch.setattr(fetch_mod.requests, "get", lambda url, **kw: R())
    assert main(["--self-check"]) == EXIT_OK
    assert "Mindestens ein Spiegel antwortet" in capsys.readouterr().out


def test_vollstaendiger_lauf_schreibt_csv(tmp_path, monkeypatch, overpass_payload):
    monkeypatch.setattr(
        fetch_mod.requests,
        "post",
        lambda url, **kw: type(
            "R",
            (),
            {
                "status_code": 200,
                "ok": True,
                "text": "",
                "json": lambda self: overpass_payload,
            },
        )(),
    )
    target = tmp_path / "leads.csv"
    assert main(["--categories", "friseur,baeckerei", "-o", str(target)]) == EXIT_OK

    with target.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter=";"))
    assert len(rows) == 6
    assert {"name", "adresse", "telefon"} <= set(rows[0])


def test_limit_kuerzt_die_ausgabe(tmp_path, monkeypatch, overpass_payload):
    monkeypatch.setattr(
        fetch_mod.requests,
        "post",
        lambda url, **kw: type(
            "R",
            (),
            {
                "status_code": 200,
                "ok": True,
                "text": "",
                "json": lambda self: overpass_payload,
            },
        )(),
    )
    target = tmp_path / "leads.csv"
    main(["--limit", "2", "-o", str(target)])
    with target.open(encoding="utf-8-sig", newline="") as handle:
        assert len(list(csv.DictReader(handle, delimiter=";"))) == 2


def test_netzsperre_im_normallauf_hat_eigenen_exitcode(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(
        fetch_mod.requests,
        "post",
        lambda url, **kw: (_ for _ in ()).throw(requests.ConnectionError()),
    )
    code = main(["-o", str(tmp_path / "x.csv")])
    assert code == EXIT_UNREACHABLE
    assert "--self-check" in capsys.readouterr().err


def test_statistik_landet_auf_stderr_nicht_in_der_csv(
    tmp_path, monkeypatch, overpass_payload, capsys
):
    monkeypatch.setattr(
        fetch_mod.requests,
        "post",
        lambda url, **kw: type(
            "R",
            (),
            {
                "status_code": 200,
                "ok": True,
                "text": "",
                "json": lambda self: overpass_payload,
            },
        )(),
    )
    main(["-o", str(tmp_path / "leads.csv")])
    captured = capsys.readouterr()
    assert "brauchbare Leads" in captured.err
    assert "OpenStreetMap" in captured.err


def test_from_file_arbeitet_ohne_netz(tmp_path, monkeypatch, capsys):
    """Ermöglicht den Lauf dort, wo Overpass gesperrt ist.

    Antwort anderswo speichern (z. B. overpass-turbo.eu), hier auswerten.
    """
    from pathlib import Path as P

    fixture = P(__file__).parent / "fixtures" / "overpass_muenchen.json"
    saved = tmp_path / "antwort.json"
    saved.write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")

    def explode(*args, **kwargs):
        raise AssertionError("--from-file darf nichts senden")

    monkeypatch.setattr(fetch_mod.requests, "post", explode)
    monkeypatch.setattr(fetch_mod.requests, "get", explode)

    target = tmp_path / "leads.csv"
    assert main(["--from-file", str(saved), "-o", str(target)]) == EXIT_OK

    with target.open(encoding="utf-8-sig", newline="") as handle:
        assert len(list(csv.DictReader(handle, delimiter=";"))) == 6
    assert "kein Netzzugriff" in capsys.readouterr().err


def test_from_file_kaputte_datei_ist_fehler(tmp_path, capsys):
    bad = tmp_path / "kaputt.json"
    bad.write_text("{ kein json", encoding="utf-8")
    assert main(["--from-file", str(bad), "-o", str(tmp_path / "x.csv")]) == EXIT_ERROR
    assert "nicht lesbar" in capsys.readouterr().err


# --- Google-Provider ---------------------------------------------------------

GKEY = "AIza-CLI-GEHEIM-0815"


def _google_response(payload):
    return type(
        "R",
        (),
        {
            "status_code": 200,
            "ok": True,
            "text": "",
            "json": lambda self: payload,
        },
    )()


def test_google_dry_run_braucht_keinen_key_und_sendet_nichts(
    capsys, monkeypatch
):
    from leadfinder import google as g

    monkeypatch.delenv("GOOGLE_MAPS_API_KEY", raising=False)
    monkeypatch.setattr(
        g.requests,
        "post",
        lambda *a, **kw: (_ for _ in ()).throw(
            AssertionError("dry-run darf nichts senden")
        ),
    )
    assert main(["--provider", "google", "--dry-run", "--categories", "friseur",
                 "--grid", "4"]) == EXIT_OK

    out = capsys.readouterr().out
    assert "4×4 = 16" in out
    assert "Mindestens 16 Abfragen" in out
    assert "places.websiteUri" in out


def test_google_ohne_key_erklaert_die_umgebungsvariable(capsys, monkeypatch):
    monkeypatch.delenv("GOOGLE_MAPS_API_KEY", raising=False)
    assert main(["--provider", "google", "--categories", "friseur"]) == EXIT_ERROR
    err = capsys.readouterr().err
    assert "GOOGLE_MAPS_API_KEY" in err
    assert "ps" in err  # Begründung, warum kein CLI-Argument


def test_google_vollstaendiger_lauf(tmp_path, monkeypatch, capsys):
    import json as _json
    from pathlib import Path as P

    from leadfinder import google as g

    pages = _json.loads(
        (P(__file__).parent / "fixtures" / "google_places.json").read_text(
            encoding="utf-8"
        )
    )
    monkeypatch.setenv("GOOGLE_MAPS_API_KEY", GKEY)
    monkeypatch.setattr(
        g.requests, "post", lambda *a, **kw: _google_response(pages["page1"])
    )

    target = tmp_path / "leads.csv"
    code = main([
        "--provider", "google", "--categories", "friseur", "--grid", "1",
        "--budget-file", str(tmp_path / "b.json"), "-o", str(target),
    ])
    assert code == EXIT_OK

    with target.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter=";"))
    assert [r["name"] for r in rows] == ["Friseursalon Wagner"]
    assert rows[0]["quelle"] == "Google Maps Platform (Places API)"
    assert rows[0]["telefon"] == "+498912345678"


def test_google_key_taucht_in_keiner_ausgabe_auf(tmp_path, monkeypatch, capsys):
    """Der Chat-, Log- und Terminalverlauf darf den Key nicht enthalten."""
    import json as _json
    from pathlib import Path as P

    from leadfinder import google as g

    pages = _json.loads(
        (P(__file__).parent / "fixtures" / "google_places.json").read_text(
            encoding="utf-8"
        )
    )
    monkeypatch.setenv("GOOGLE_MAPS_API_KEY", GKEY)
    monkeypatch.setattr(
        g.requests, "post", lambda *a, **kw: _google_response(pages["page1"])
    )

    target = tmp_path / "leads.csv"
    main([
        "--provider", "google", "--categories", "friseur", "--grid", "1",
        "--budget-file", str(tmp_path / "b.json"), "-o", str(target),
    ])
    captured = capsys.readouterr()
    assert GKEY not in captured.out
    assert GKEY not in captured.err
    assert GKEY not in target.read_text(encoding="utf-8-sig")


def test_google_budget_erschoepft_bricht_vorher_ab(tmp_path, monkeypatch, capsys):
    from leadfinder.budget import Budget

    monkeypatch.setenv("GOOGLE_MAPS_API_KEY", GKEY)
    budget_file = tmp_path / "b.json"
    Budget(limit=5, path=budget_file).spend(5)

    code = main([
        "--provider", "google", "--categories", "friseur",
        "--max-requests-month", "5", "--budget-file", str(budget_file),
        "-o", str(tmp_path / "leads.csv"),
    ])
    assert code == EXIT_ERROR
    assert "5/5" in capsys.readouterr().err


def test_google_self_check_erkennt_netzsperre(capsys, monkeypatch):
    from leadfinder import google as g

    monkeypatch.delenv("GOOGLE_MAPS_API_KEY", raising=False)
    monkeypatch.setattr(
        g.requests,
        "post",
        lambda *a, **kw: (_ for _ in ()).throw(requests.ConnectionError()),
    )
    assert main(["--provider", "google", "--self-check"]) == EXIT_UNREACHABLE
    assert "nicht durch" in capsys.readouterr().out


def test_google_self_check_ohne_key_meldet_erreichbar(capsys, monkeypatch):
    """Googles PERMISSION_DENIED ist hier die gute Nachricht."""
    from leadfinder import google as g

    monkeypatch.delenv("GOOGLE_MAPS_API_KEY", raising=False)
    monkeypatch.setattr(
        g.requests,
        "post",
        lambda *a, **kw: type(
            "R",
            (),
            {"status_code": 403, "ok": False,
             "text": '{"error":{"status":"PERMISSION_DENIED"}}',
             "json": lambda self: {}},
        )(),
    )
    assert main(["--provider", "google", "--self-check"]) == EXIT_OK
    out = capsys.readouterr().out
    assert "Endpunkt erreichbar" in out
