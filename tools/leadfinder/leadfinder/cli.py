"""Kommandozeile.

Drei Betriebsarten, weil in gesperrten Netzen die häufigste Frage nicht
"was sind die Ergebnisse" ist, sondern "warum kommen keine":
`--self-check` beantwortet das direkt, `--dry-run` zeigt die Abfrage ohne sie
zu senden, und der Normallauf trennt Netzfehler (Exit 2) sauber von echten
Fehlern (Exit 1).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import categories as cats
from . import fetch as fetch_mod
from .export import ATTRIBUTION, write_csv
from .parse import parse_elements
from .query import build_query

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_UNREACHABLE = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="leadfinder",
        description=(
            "Findet lokale Betriebe ohne eingetragene Webseite in "
            "OpenStreetMap und schreibt sie als CSV."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Beispiele:\n"
            "  leadfinder --self-check\n"
            "  leadfinder --dry-run --categories friseur\n"
            "  leadfinder --categories friseur,baeckerei --limit 100 "
            "-o leads.csv\n"
        ),
    )
    parser.add_argument(
        "--categories",
        default=",".join(cats.DEFAULT_CATEGORIES),
        help="Branchen, kommagetrennt (Standard: %(default)s)",
    )
    parser.add_argument("--area", default="München", help="Gebiet (Standard: München)")
    parser.add_argument("--limit", type=int, help="Höchstzahl Leads in der Ausgabe")
    parser.add_argument("-o", "--output", default="leads.csv", help="Zieldatei")
    parser.add_argument("--delimiter", default=";", help="CSV-Trenner (Standard: ;)")
    parser.add_argument(
        "--no-require-phone",
        action="store_true",
        help="auch Betriebe ohne Telefonnummer aufnehmen",
    )
    parser.add_argument("--mirror", action="append", help="Overpass-Spiegel überschreiben")
    parser.add_argument("--timeout", type=int, default=180, help="Overpass-Timeout (s)")
    parser.add_argument(
        "--user-agent",
        default=fetch_mod.DEFAULT_USER_AGENT,
        help="User-Agent; bitte echte Kontaktadresse eintragen",
    )
    parser.add_argument(
        "--from-file",
        help=(
            "gespeicherte Overpass-JSON-Antwort auswerten statt abzufragen "
            "(z. B. Export aus overpass-turbo.eu) — funktioniert ohne Netz"
        ),
    )
    parser.add_argument("--dry-run", action="store_true", help="nur die Abfrage zeigen")
    parser.add_argument("--self-check", action="store_true", help="Erreichbarkeit prüfen")
    parser.add_argument(
        "--list-categories", action="store_true", help="Branchen auflisten"
    )
    return parser


def _self_check(mirrors: tuple[str, ...], user_agent: str) -> int:
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


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    mirrors = tuple(args.mirror) if args.mirror else fetch_mod.MIRRORS

    if args.list_categories:
        print("Verfügbare Branchen:\n")
        for slug, cat in sorted(cats.CATEGORIES.items()):
            tags = ", ".join(f"{k}={v}" for k, v in cat.selectors)
            print(f"  {slug:<12} {cat.label:<14} {tags}")
        return EXIT_OK

    if args.self_check:
        return _self_check(mirrors, args.user_agent)

    try:
        selected = cats.resolve([s.strip() for s in args.categories.split(",") if s.strip()])
        query = build_query(selected, area_name=args.area, timeout=args.timeout)
    except ValueError as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return EXIT_ERROR

    if args.dry_run:
        print(query)
        return EXIT_OK

    if args.from_file:
        try:
            payload = json.loads(Path(args.from_file).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"Fehler: {args.from_file} nicht lesbar — {exc}", file=sys.stderr)
            return EXIT_ERROR
        print(f"Werte {args.from_file} aus (kein Netzzugriff) …", file=sys.stderr)
    else:
        print(
            f"Frage Overpass nach {len(selected)} Branche(n) in {args.area} …",
            file=sys.stderr,
        )
        try:
            payload = fetch_mod.fetch(
                query, mirrors=mirrors, user_agent=args.user_agent
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

    leads, stats = parse_elements(
        payload.get("elements", []), require_phone=not args.no_require_phone
    )
    if args.limit is not None:
        leads = leads[: args.limit]

    target = write_csv(leads, args.output, delimiter=args.delimiter)

    print("\nErgebnis:", file=sys.stderr)
    for line in stats.as_lines():
        print(line, file=sys.stderr)
    print(f"\nGeschrieben: {target}  ({len(leads)} Zeilen)", file=sys.stderr)
    print(f"Datenquelle: {ATTRIBUTION}", file=sys.stderr)
    if not leads:
        print(
            "\nKeine Leads. Bei OSM ist das oft echt und nicht kaputt: "
            "prüfe mit\n--list-categories die Tag-Werte und mit --dry-run das "
            "Gebiet.",
            file=sys.stderr,
        )
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
