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


# --- Browser-Brücke ----------------------------------------------------------


def test_turbo_link_url_steht_allein_auf_ihrer_zeile(capsys, monkeypatch):
    """Beschriftung darüber, URL darunter — sonst lässt sie sich nicht
    sauber kopieren."""
    monkeypatch.setattr(
        fetch_mod.requests,
        "post",
        lambda *a, **kw: (_ for _ in ()).throw(AssertionError("darf nichts senden")),
    )
    assert main(["--turbo-link", "--categories", "friseur"]) == EXIT_OK

    zeilen = [z for z in capsys.readouterr().out.splitlines() if z.strip()]
    assert zeilen[0] == "[1/1] Friseur"
    assert zeilen[1].startswith("https://overpass-turbo.eu/?Q=")
    assert len(zeilen) == 2


def test_dry_run_haengt_den_turbo_link_an(capsys, monkeypatch):
    monkeypatch.setattr(
        fetch_mod.requests,
        "post",
        lambda *a, **kw: (_ for _ in ()).throw(AssertionError("darf nichts senden")),
    )
    main(["--dry-run", "--categories", "friseur"])
    out = capsys.readouterr().out
    assert 'nwr["shop"="hairdresser"]' in out
    assert "overpass-turbo.eu" in out


def test_turbo_link_gibt_es_bei_google_nicht(capsys):
    assert main(["--provider", "google", "--turbo-link"]) == EXIT_ERROR
    assert "nur für --provider overpass" in capsys.readouterr().err


def test_geojson_export_ergibt_dieselbe_csv_wie_die_api_antwort(tmp_path):
    """Der Regressionsnachweis auf CLI-Ebene: vorher 6 gegen 0."""
    from pathlib import Path as P

    fixtures = P(__file__).parent / "fixtures"
    ergebnisse = []
    for name in ("overpass_muenchen.json", "overpass_turbo_geojson.json"):
        ziel = tmp_path / f"{name}.csv"
        assert main(["--from-file", str(fixtures / name), "-o", str(ziel)]) == EXIT_OK
        with ziel.open(encoding="utf-8-sig", newline="") as handle:
            ergebnisse.append([r["name"] for r in csv.DictReader(handle, delimiter=";")])

    assert ergebnisse[0] == ergebnisse[1]
    assert len(ergebnisse[0]) == 6


def test_unbekanntes_dateiformat_wird_erklaert(tmp_path, capsys):
    """Früher: still null Leads. Das sah aus wie 'München hat nichts'."""
    datei = tmp_path / "fremd.json"
    datei.write_text('{"ergebnisse": [1, 2]}', encoding="utf-8")

    code = main(["--from-file", str(datei), "-o", str(tmp_path / "x.csv")])
    assert code == EXIT_ERROR
    err = capsys.readouterr().err
    assert "elements" in err and "features" in err


def test_leere_datei_nennt_den_wahrscheinlichen_grund(tmp_path, capsys):
    datei = tmp_path / "leer.json"
    datei.write_text('{"features": []}', encoding="utf-8")

    assert main(["--from-file", str(datei), "-o", str(tmp_path / "x.csv")]) == EXIT_OK
    assert "Keine Elemente in den Eingabedaten" in capsys.readouterr().err


def test_social_spalte_landet_in_der_csv(tmp_path):
    from pathlib import Path as P

    fixture = P(__file__).parent / "fixtures" / "overpass_turbo_geojson.json"
    ziel = tmp_path / "leads.csv"
    main(["--from-file", str(fixture), "-o", str(ziel)])

    with ziel.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter=";"))

    assert "social" in rows[0]
    assert rows[0]["social"]  # Social-Leads stehen oben
    assert any("facebook" in r["social"] for r in rows)


# --- Aufteilung und Zusammenführung ------------------------------------------


def _kein_netz(monkeypatch):
    for name in ("post", "get"):
        monkeypatch.setattr(
            fetch_mod.requests,
            name,
            lambda *a, **kw: (_ for _ in ()).throw(AssertionError("darf nichts senden")),
        )


def test_split_erzeugt_mehrere_beschriftete_links(capsys, monkeypatch):
    """Ein Link für alle Branchen wäre über 4000 Zeichen lang und würde bei
    Overpass ohnehin in den Timeout laufen."""
    _kein_netz(monkeypatch)
    assert main([
        "--turbo-link", "--split", "2",
        "--categories", "friseur,baeckerei,kosmetik,metzger,blumen",
    ]) == EXIT_OK

    out = capsys.readouterr().out
    assert out.count("https://overpass-turbo.eu/?Q=") == 3
    assert "[1/3]" in out and "[3/3]" in out
    assert "Metzgerei" in out


def test_jeder_link_dekodiert_verlustfrei_zurueck(capsys, monkeypatch):
    from urllib.parse import parse_qs, urlparse

    _kein_netz(monkeypatch)
    main(["--turbo-link", "--split", "3", "--categories",
          "friseur,baeckerei,kosmetik,metzger,blumen,optiker"])

    urls = [
        z for z in capsys.readouterr().out.splitlines()
        if z.startswith("https://")
    ]
    assert len(urls) == 2
    for url in urls:
        abfrage = parse_qs(urlparse(url).query)["Q"][0]
        assert abfrage.startswith("[out:json]")
        assert abfrage.rstrip().endswith("out center tags;")
        assert len(url) < 4000


def test_mehrere_dateien_werden_zusammengefuehrt(tmp_path, monkeypatch, capsys):
    """Vier Downloads sollen eine CSV ergeben."""
    from pathlib import Path as P

    _kein_netz(monkeypatch)
    fixtures = P(__file__).parent / "fixtures"
    ziel = tmp_path / "leads.csv"

    assert main([
        "--from-file", str(fixtures / "overpass_muenchen.json"),
        "--from-file", str(fixtures / "overpass_turbo_geojson.json"),
        "-o", str(ziel),
    ]) == EXIT_OK

    with ziel.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter=";"))

    # Beide Dateien enthalten dieselben Betriebe: die Deduplizierung über die
    # OSM-ID muss greifen, sonst stünde jeder Lead doppelt in der Liste.
    assert len(rows) == 6
    assert "2 Datei(en)" in capsys.readouterr().err


def test_fehler_in_der_zweiten_datei_nennt_den_dateinamen(tmp_path, capsys):
    from pathlib import Path as P

    gut = P(__file__).parent / "fixtures" / "overpass_muenchen.json"
    schlecht = tmp_path / "fremd.json"
    schlecht.write_text('{"was_anderes": []}', encoding="utf-8")

    code = main([
        "--from-file", str(gut), "--from-file", str(schlecht),
        "-o", str(tmp_path / "x.csv"),
    ])
    assert code == EXIT_ERROR
    assert "fremd.json" in capsys.readouterr().err


def test_branchen_ohne_treffer_werden_gemeldet(tmp_path, monkeypatch, capsys):
    """Null Treffer heißt fast immer falscher Tag-Wert — das muss auffallen."""
    from pathlib import Path as P

    _kein_netz(monkeypatch)
    fixture = P(__file__).parent / "fixtures" / "overpass_muenchen.json"
    main([
        "--from-file", str(fixture),
        "--categories", "friseur,tierarzt,fahrschule",
        "-o", str(tmp_path / "leads.csv"),
    ])
    err = capsys.readouterr().err
    assert "ohne jeden Treffer" in err
    assert "Tierarzt" in err and "Fahrschule" in err


def test_area_id_landet_in_der_abfrage(capsys, monkeypatch):
    _kein_netz(monkeypatch)
    main(["--dry-run", "--categories", "friseur", "--area-id", "62428"])
    assert "area(3600062428)" in capsys.readouterr().out


def test_live_abruf_fragt_je_gruppe_einmal(tmp_path, monkeypatch, overpass_payload):
    """Sonst gälte das Timeout-Argument nur für den Browser-Weg.

    Mehrere kleine Abfragen sind gegenüber einem Spendendienst auch das
    anständigere Verhalten.
    """
    abfragen = []

    def fake_post(url, **kw):
        abfragen.append(kw["data"]["data"])
        return type(
            "R",
            (),
            {"status_code": 200, "ok": True, "text": "",
             "json": lambda self: overpass_payload},
        )()

    monkeypatch.setattr(fetch_mod.requests, "post", fake_post)
    main([
        "--categories", "friseur,baeckerei,kosmetik,metzger,blumen",
        "--split", "2", "-o", str(tmp_path / "leads.csv"),
    ])

    assert len(abfragen) == 3
    assert 'nwr["shop"="hairdresser"]' in abfragen[0]
    assert 'nwr["shop"="florist"]' in abfragen[2]


def test_live_abruf_dedupliziert_ueber_die_gruppen(tmp_path, monkeypatch, overpass_payload):
    """Dieselbe Antwort dreimal darf nicht dreifache Leads ergeben."""
    monkeypatch.setattr(
        fetch_mod.requests,
        "post",
        lambda url, **kw: type(
            "R",
            (),
            {"status_code": 200, "ok": True, "text": "",
             "json": lambda self: overpass_payload},
        )(),
    )
    ziel = tmp_path / "leads.csv"
    main([
        "--categories", "friseur,baeckerei,kosmetik,metzger,blumen",
        "--split", "2", "-o", str(ziel),
    ])
    with ziel.open(encoding="utf-8-sig", newline="") as handle:
        assert len(list(csv.DictReader(handle, delimiter=";"))) == 6
