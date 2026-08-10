"""Kommandozeile.

Zwei Datenquellen mit sehr unterschiedlichem Charakter: Overpass ist gratis
und oft gesperrt, Google ist erreichbar und kostet Geld. Die CLI macht diesen
Unterschied sichtbar, statt ihn zu verstecken — beim Google-Weg gibt es
deshalb Kachelzahl, Abfrageschätzung und einen Budgetzähler zu sehen, bevor
etwas abgerechnet wird.

Exit-Codes trennen die häufigste Ursache von echten Fehlern: 2 heißt "Netz
oder Zugang", 1 heißt "Bedienung oder Daten".
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from . import budget as budget_mod
from . import categories as cats
from . import fetch as fetch_mod
from . import google as google_mod
from .export import GOOGLE_ATTRIBUTION, OSM_ATTRIBUTION, write_csv
from .ingest import UnknownFormat, normalize_payload
from .parse import parse_elements
from .query import build_query, turbo_url

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_UNREACHABLE = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="leadfinder",
        description=(
            "Findet lokale Betriebe ohne eingetragene Webseite und schreibt "
            "sie als CSV."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Beispiele:\n"
            "  leadfinder --self-check\n"
            "  leadfinder --dry-run --categories friseur\n"
            "  export GOOGLE_MAPS_API_KEY=…\n"
            "  leadfinder --provider google --dry-run --categories friseur\n"
            "  leadfinder --provider google --categories friseur "
            "--max-requests-month 50 -o leads.csv\n"
        ),
    )
    parser.add_argument(
        "--provider",
        choices=("overpass", "google"),
        default="overpass",
        help="Datenquelle (Standard: overpass, gratis aber oft gesperrt)",
    )
    parser.add_argument(
        "--categories",
        default=",".join(cats.DEFAULT_CATEGORIES),
        help="Branchen, kommagetrennt (Standard: %(default)s)",
    )
    parser.add_argument("--area", default="München", help="Gebiet (nur overpass)")
    parser.add_argument("--limit", type=int, help="Höchstzahl Leads in der Ausgabe")
    parser.add_argument("-o", "--output", default="leads.csv", help="Zieldatei")
    parser.add_argument("--delimiter", default=";", help="CSV-Trenner (Standard: ;)")
    parser.add_argument(
        "--no-require-phone",
        action="store_true",
        help="auch Betriebe ohne Telefonnummer aufnehmen",
    )

    overpass = parser.add_argument_group("overpass")
    overpass.add_argument("--mirror", action="append", help="Spiegel überschreiben")
    overpass.add_argument("--timeout", type=int, default=180, help="Overpass-Timeout")
    overpass.add_argument(
        "--user-agent",
        default=fetch_mod.DEFAULT_USER_AGENT,
        help="User-Agent; bitte echte Kontaktadresse eintragen",
    )
    overpass.add_argument(
        "--from-file",
        action="append",
        metavar="DATEI",
        help=(
            "gespeicherte Antwort auswerten (ohne Netz). Nimmt Overpass-JSON "
            "und GeoJSON aus overpass-turbo. Mehrfach angebbar — die Exporte "
            "werden zusammengeführt und über die OSM-ID dedupliziert."
        ),
    )
    overpass.add_argument(
        "--area-id",
        type=int,
        metavar="RELATION",
        help=(
            "Gebiet auf eine OSM-Relation pinnen statt über den Namen zu "
            "suchen. Nötig, wenn im Ergebnis Orte aus dem Umland auftauchen: "
            "gleichnamige Flächen derselben Verwaltungsstufe werden von "
            "Overpass sonst vereinigt."
        ),
    )
    overpass.add_argument(
        "--split",
        type=int,
        default=4,
        metavar="N",
        help=(
            "Branchen je Link/Abfrage (Standard: %(default)s). Eine Abfrage "
            "über ganz München mit allen Branchen läuft in den Timeout und "
            "ergibt eine überlange URL."
        ),
    )
    overpass.add_argument(
        "--turbo-link",
        action="store_true",
        help=(
            "nur den overpass-turbo-Link ausgeben: anklicken, laufen "
            "lassen, exportieren, mit --from-file auswerten"
        ),
    )

    google = parser.add_argument_group("google")
    google.add_argument(
        "--grid",
        type=int,
        default=3,
        help=(
            "Stadtgebiet in N×N Kacheln zerlegen (Standard: 3). Wichtigster "
            "Kostenhebel: die Abfragezahl wächst quadratisch."
        ),
    )
    google.add_argument(
        "--max-pages",
        type=int,
        default=1,
        help="Seiten je Kachel, max. 3 (Standard: 1 — jede Seite kostet extra)",
    )
    google.add_argument(
        "--max-requests-month",
        type=int,
        default=budget_mod.DEFAULT_LIMIT,
        help="harte Monatsgrenze für Abfragen (Standard: %(default)s)",
    )
    google.add_argument(
        "--budget-file",
        default=str(budget_mod.DEFAULT_PATH),
        help="Datei für den Abfragezähler",
    )
    google.add_argument(
        "--api-key-env",
        default="GOOGLE_MAPS_API_KEY",
        help=(
            "Umgebungsvariable mit dem API-Key (Standard: %(default)s). "
            "Der Key wird bewusst nicht als Argument entgegengenommen — "
            "Kommandozeilen sind über ps für andere sichtbar."
        ),
    )

    parser.add_argument("--dry-run", action="store_true", help="nur zeigen, nichts senden")
    parser.add_argument("--self-check", action="store_true", help="Erreichbarkeit prüfen")
    parser.add_argument(
        "--list-categories", action="store_true", help="Branchen auflisten"
    )
    return parser


def _self_check_overpass(mirrors, user_agent: str) -> int:
    print("Erreichbarkeit der Overpass-Spiegel:\n")
    results = fetch_mod.check_reachability(mirrors, user_agent=user_agent)
    for mirror, status in results:
        marker = "ok     " if status == "ok" else "FEHLER "
        print(f"  {marker} {mirror}  ({status})")

    if any(status == "ok" for _, status in results):
        print("\nMindestens ein Spiegel antwortet. Der Normallauf sollte gehen.")
        return EXIT_OK

    print(
        "\nKein Spiegel erreichbar. Das ist fast immer eine Netzsperre und "
        "kein Fehler\ndieses Tools — in abgeschotteten Containern und hinter "
        "Firmen-Proxys ist\nOverpass regelmäßig blockiert. Führe den Lauf auf "
        "einem Rechner mit freiem\nInternetzugang aus."
    )
    return EXIT_UNREACHABLE


def _self_check_google(api_key: str) -> int:
    """Ohne Key prüfen, ob der Endpunkt überhaupt antwortet.

    Googles "PERMISSION_DENIED" ist hier die *gute* Nachricht: sie belegt,
    dass Netz und URL stimmen und nur der Key fehlt. Eine Netzsperre sieht
    völlig anders aus.
    """
    print(f"Google Places: {google_mod.ENDPOINT}\n")
    try:
        google_mod.search_page(
            "Friseur", google_mod.MUENCHEN, api_key or "", timeout=20
        )
    except google_mod.GoogleUnreachable as exc:
        print(f"  FEHLER  {exc}")
        print("\nDas Netz lässt Google Places nicht durch.")
        return EXIT_UNREACHABLE
    except google_mod.GoogleAuthError:
        if api_key:
            print("  FEHLER  Endpunkt erreichbar, aber der Key wird abgelehnt.")
            print(
                "\nPrüfe: Ist \"Places API (New)\" im Projekt aktiviert? "
                "Sind die\nKey-Beschränkungen (API/IP) zu eng? Ist die "
                "Abrechnung eingerichtet?"
            )
            return EXIT_ERROR
        print("  ok      Endpunkt erreichbar (Google verlangt einen Key)")
        print(
            "\nNetz und URL stimmen. Setze den Key und starte den echten Lauf:"
            "\n  export GOOGLE_MAPS_API_KEY=…"
        )
        return EXIT_OK
    except google_mod.GoogleError as exc:
        print(f"  FEHLER  {exc}")
        return EXIT_ERROR

    print("  ok      Endpunkt erreichbar, Key akzeptiert")
    return EXIT_OK


def _run_overpass(args, selected) -> tuple[int, list, object] | int:
    def _query(gruppe):
        return build_query(
            gruppe,
            area_name=args.area,
            timeout=args.timeout,
            area_id=args.area_id,
        )

    gruppen = cats.in_gruppen(selected, max(1, args.split))

    if args.turbo_link:
        _print_links(gruppen, _query)
        return EXIT_OK

    if args.dry_run:
        for gruppe in gruppen:
            print(_query(gruppe))
        print("Im Browser ausführen (falls Overpass hier gesperrt ist):\n")
        _print_links(gruppen, _query)
        return EXIT_OK

    if args.from_file:
        elements: list[dict] = []
        for pfad in args.from_file:
            try:
                payload = json.loads(Path(pfad).read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                print(f"Fehler: {pfad} nicht lesbar — {exc}", file=sys.stderr)
                return EXIT_ERROR
            try:
                teil = normalize_payload(payload)
            except UnknownFormat as exc:
                print(f"\nFehler in {pfad}: {exc}", file=sys.stderr)
                return EXIT_ERROR
            print(
                f"  {pfad}: {len(teil)} Elemente", file=sys.stderr
            )
            elements.extend(teil)
        print(
            f"Werte {len(args.from_file)} Datei(en) aus, {len(elements)} "
            "Elemente gesamt (kein Netzzugriff) …",
            file=sys.stderr,
        )
        return _auswerten(elements, args, selected)

    # Auch der Live-Abruf geht gruppenweise. Eine Abfrage über ganz München
    # mit allen Branchen läuft in den Timeout, und mehrere kleine Abfragen
    # sind gegenüber einem Spendendienst das anständigere Verhalten.
    print(
        f"Frage Overpass nach {len(selected)} Branche(n) in {args.area}, "
        f"in {len(gruppen)} Abfrage(n) …",
        file=sys.stderr,
    )
    mirrors = tuple(args.mirror) if args.mirror else fetch_mod.MIRRORS
    elements = []
    for nummer, gruppe in enumerate(gruppen, 1):
        namen = ", ".join(cat.label for cat in gruppe)
        print(f"  [{nummer}/{len(gruppen)}] {namen} …", file=sys.stderr)
        try:
            payload = fetch_mod.fetch(
                _query(gruppe), mirrors=mirrors, user_agent=args.user_agent
            )
        except fetch_mod.OverpassUnreachable as exc:
            print(f"\nFehler: {exc}", file=sys.stderr)
            print(
                "Prüfe mit --self-check, ob das Netz Overpass überhaupt zulässt.",
                file=sys.stderr,
            )
            return EXIT_UNREACHABLE
        except fetch_mod.OverpassError as exc:
            print(f"\nFehler: {exc}", file=sys.stderr)
            return EXIT_ERROR

        try:
            elements.extend(normalize_payload(payload))
        except UnknownFormat as exc:
            print(f"\nFehler: {exc}", file=sys.stderr)
            return EXIT_ERROR

    return _auswerten(elements, args, selected)


def _print_links(gruppen, bauen) -> None:
    """Je Gruppe ein nummerierter Link, beschriftet mit den Branchen.

    Ein Link für alles wäre über 4000 Zeichen lang und würde bei Overpass
    ohnehin in den Timeout laufen.
    """
    for nummer, gruppe in enumerate(gruppen, 1):
        namen = ", ".join(cat.label for cat in gruppe)
        url = turbo_url(bauen(gruppe))
        print(f"[{nummer}/{len(gruppen)}] {namen}")
        print(url)
        if len(url) > 4000:
            print(
                "  Achtung: sehr lange URL — mit kleinerem --split aufteilen, "
                "falls der Browser sie abschneidet"
            )
        print()


def _auswerten(elements, args, selected):
    if not elements:
        # Früher endete das hier stumm mit null Leads — nicht unterscheidbar
        # von "es gibt nichts". Jetzt wird der wahrscheinlichste Grund genannt.
        print(
            "\nKeine Elemente in den Eingabedaten. Häufigste Ursache: beim "
            "Export in\noverpass-turbo lief die Abfrage noch nicht oder lieferte "
            "nichts.",
            file=sys.stderr,
        )

    leads, stats = parse_elements(
        elements, require_phone=not args.no_require_phone
    )
    # Eine Branche ohne einen einzigen Treffer ist meistens ein falscher
    # OSM-Tag-Wert — der wirft keinen Fehler, er liefert nur nichts.
    stats.leere_branchen = [
        cat.label for cat in selected if cat.label not in stats.kategorien
    ]
    return leads, stats, OSM_ATTRIBUTION


def _run_google(args, selected):
    grid_tiles = google_mod.tiles(grid=args.grid)
    estimate = google_mod.estimate_requests(
        len(selected), args.grid, args.max_pages
    )

    if args.dry_run:
        print(f"Provider:      Google Places (New), {google_mod.ENDPOINT}")
        print(f"Gebiet:        München {google_mod.MUENCHEN}")
        print(f"Kacheln:       {args.grid}×{args.grid} = {len(grid_tiles)}")
        print(f"Branchen:      {', '.join(c.label for c in selected)}")
        print(f"Seiten/Kachel: {args.max_pages}")
        print(f"\nMindestens {estimate} Abfragen — jede kostet Geld.")
        print("Feldmaske:")
        for field in google_mod.FIELD_MASK.split(","):
            print(f"  {field}")
        print("\nSuchtexte:")
        for cat in selected:
            print(f"  {cat.label!r} je Kachel")
        return EXIT_OK

    api_key = os.environ.get(args.api_key_env, "").strip()
    if not api_key:
        print(
            f"Fehler: Umgebungsvariable {args.api_key_env} ist nicht gesetzt.\n"
            f"  export {args.api_key_env}=\"dein-key\"\n"
            "Der Key wird absichtlich nicht als Argument angenommen — "
            "Kommandozeilen\nsind über ps für andere Nutzer sichtbar.",
            file=sys.stderr,
        )
        return EXIT_ERROR

    budget = budget_mod.Budget(
        limit=args.max_requests_month, path=args.budget_file
    )
    if budget.remaining <= 0:
        print(f"Fehler: {budget.status()}.", file=sys.stderr)
        return EXIT_ERROR

    print(
        f"Google Places: {len(selected)} Branche(n) × {len(grid_tiles)} "
        f"Kacheln, mindestens {estimate} Abfragen.\n"
        f"Budget: {budget.status()}, {budget.remaining} übrig.",
        file=sys.stderr,
    )

    try:
        leads, stats = google_mod.collect(
            selected,
            api_key,
            budget,
            grid=args.grid,
            require_phone=not args.no_require_phone,
            max_pages=max(1, min(args.max_pages, google_mod.MAX_PAGES)),
        )
    except google_mod.GoogleUnreachable as exc:
        print(f"\nFehler: {exc}", file=sys.stderr)
        return EXIT_UNREACHABLE
    except google_mod.GoogleAuthError as exc:
        print(f"\nFehler: {exc}", file=sys.stderr)
        return EXIT_ERROR
    except google_mod.GoogleError as exc:
        print(f"\nFehler: {exc}", file=sys.stderr)
        return EXIT_ERROR

    print(f"Budget danach: {budget.status()}.", file=sys.stderr)
    return leads, stats, GOOGLE_ATTRIBUTION


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.list_categories:
        print("Verfügbare Branchen:\n")
        for slug, cat in sorted(cats.CATEGORIES.items()):
            tags = ", ".join(f"{k}={v}" for k, v in cat.selectors)
            print(f"  {slug:<12} {cat.label:<14} {tags}")
        return EXIT_OK

    if args.turbo_link and args.provider == "google":
        print(
            "Fehler: --turbo-link gibt es nur für --provider overpass.",
            file=sys.stderr,
        )
        return EXIT_ERROR

    if args.self_check:
        if args.provider == "google":
            return _self_check_google(os.environ.get(args.api_key_env, "").strip())
        mirrors = tuple(args.mirror) if args.mirror else fetch_mod.MIRRORS
        return _self_check_overpass(mirrors, args.user_agent)

    try:
        selected = cats.resolve(
            [s.strip() for s in args.categories.split(",") if s.strip()]
        )
    except ValueError as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return EXIT_ERROR

    try:
        result = (
            _run_google(args, selected)
            if args.provider == "google"
            else _run_overpass(args, selected)
        )
    except ValueError as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return EXIT_ERROR

    if isinstance(result, int):
        return result

    leads, stats, quelle = result
    if args.limit is not None:
        leads = leads[: args.limit]

    target = write_csv(
        leads, args.output, delimiter=args.delimiter, quelle=quelle
    )

    print("\nErgebnis:", file=sys.stderr)
    for line in stats.as_lines():
        print(line, file=sys.stderr)
    print(f"\nGeschrieben: {target}  ({len(leads)} Zeilen)", file=sys.stderr)
    print(f"Datenquelle: {quelle}", file=sys.stderr)
    if not leads:
        print(
            "\nKeine Leads. Das ist oft echt und nicht kaputt: prüfe mit\n"
            "--list-categories die Branchen und mit --dry-run das Gebiet.",
            file=sys.stderr,
        )
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
