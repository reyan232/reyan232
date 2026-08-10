from datetime import date

import pytest

from leadfinder.budget import Budget, BudgetExhausted


def test_frischer_zaehler_startet_bei_null(tmp_path):
    b = Budget(limit=10, path=tmp_path / "budget.json")
    assert b.used == 0
    assert b.remaining == 10


def test_spend_zaehlt_und_check_bremst(tmp_path):
    b = Budget(limit=3, path=tmp_path / "budget.json")
    for _ in range(3):
        b.check()
        b.spend()
    assert b.used == 3
    assert b.remaining == 0
    with pytest.raises(BudgetExhausted, match="Monatsgrenze erreicht"):
        b.check()


def test_zaehler_ueberlebt_neustart(tmp_path):
    """Sofort schreiben, damit ein Absturz keine Abfragen verschenkt.

    Ein zurückgesetzter Zähler heißt: dieselben Abfragen noch einmal bezahlt.
    """
    path = tmp_path / "budget.json"
    Budget(limit=10, path=path).spend(4)
    assert Budget(limit=10, path=path).used == 4


def test_monate_zaehlen_getrennt(tmp_path):
    path = tmp_path / "budget.json"
    august = Budget(limit=10, path=path, today=date(2026, 8, 15))
    august.spend(7)

    september = Budget(limit=10, path=path, today=date(2026, 9, 1))
    assert september.used == 0
    assert september.remaining == 10
    # Der alte Stand bleibt erhalten, nur eben unter seinem eigenen Monat.
    assert Budget(limit=10, path=path, today=date(2026, 8, 31)).used == 7


def test_kaputte_datei_blockiert_nicht(tmp_path):
    """Lieber bei null anfangen als den Lauf an einer Zählerdatei scheitern
    lassen — der Zähler ist eine Bremse, kein Selbstzweck."""
    path = tmp_path / "budget.json"
    path.write_text("{ kein json", encoding="utf-8")
    assert Budget(limit=5, path=path).used == 0


def test_fehlendes_verzeichnis_wird_angelegt(tmp_path):
    path = tmp_path / "tief" / "drin" / "budget.json"
    Budget(limit=5, path=path).spend()
    assert path.exists()


def test_status_nennt_monat_und_grenze(tmp_path):
    b = Budget(limit=9, path=tmp_path / "b.json", today=date(2026, 8, 10))
    b.spend(2)
    assert "2/9" in b.status()
    assert "2026-08" in b.status()
