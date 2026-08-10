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
