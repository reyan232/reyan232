import csv

from leadfinder.export import ATTRIBUTION, COLUMNS, write_csv
from leadfinder.parse import parse_elements


def test_write_csv_spalten_und_inhalt(tmp_path, elements):
    leads, _ = parse_elements(elements)
    target = write_csv(leads, tmp_path / "leads.csv")

    with target.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter=";"))

    assert list(rows[0]) == list(COLUMNS)
    assert len(rows) == len(leads)

    wagner = next(r for r in rows if r["name"] == "Friseursalon Wagner")
    assert wagner["telefon"] == "+498912345678"
    assert wagner["adresse"] == "Sendlinger Straße 12, 80331 München"
    assert wagner["kategorie"] == "Friseur"
    assert wagner["quelle"] == ATTRIBUTION


def test_write_csv_schreibt_bom_fuer_excel(tmp_path, elements):
    """Ohne BOM zeigt deutsches Excel 'Bäckerei' als 'BÃ¤ckerei'."""
    leads, _ = parse_elements(elements)
    target = write_csv(leads, tmp_path / "leads.csv")
    assert target.read_bytes().startswith(b"\xef\xbb\xbf")


def test_write_csv_umlaute_bleiben_erhalten(tmp_path, elements):
    leads, _ = parse_elements(elements)
    target = write_csv(leads, tmp_path / "leads.csv")
    text = target.read_text(encoding="utf-8-sig")
    assert "Bäckerei" in text
    assert "Sendlinger Straße" in text


def test_write_csv_trenner_konfigurierbar(tmp_path, elements):
    leads, _ = parse_elements(elements)
    target = write_csv(leads, tmp_path / "leads.csv", delimiter=",")
    first_line = target.read_text(encoding="utf-8-sig").splitlines()[0]
    assert first_line.count(",") == len(COLUMNS) - 1


def test_write_csv_legt_attribution_datei_an(tmp_path, elements):
    leads, _ = parse_elements(elements)
    write_csv(leads, tmp_path / "leads.csv")
    note = (tmp_path / "ATTRIBUTION.txt").read_text(encoding="utf-8")
    assert "ODbL" in note
    assert "OpenStreetMap" in note
    # Der wichtigste Vorbehalt gehört neben die Daten, nicht nur ins README.
    assert "belegt nicht" in note


def test_write_csv_legt_verzeichnis_an(tmp_path, elements):
    leads, _ = parse_elements(elements)
    target = write_csv(leads, tmp_path / "neu" / "tief" / "leads.csv")
    assert target.exists()


def test_write_csv_leere_liste_erzeugt_nur_kopfzeile(tmp_path):
    target = write_csv([], tmp_path / "leer.csv")
    lines = target.read_text(encoding="utf-8-sig").strip().splitlines()
    assert len(lines) == 1
