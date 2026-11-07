#!/usr/bin/env python3
"""Metadaten-Nachweis über die Crossref-REST-API (nur Finder/Verifikation, keine Fachevidenz).

Für den Orchestrator: Subagents können in der Cloud-Umgebung keine Metadatendienste
erreichen; dieses Skript läuft über die Kommandozeile (HTTPS-Proxy) und liefert
überprüfbare Metadaten für `metadata_status` / `metadata_evidence` in literature.csv.

Aufruf:
    python3 scripts/crossref_lookup.py doi 10.1108/JAAR-10-2020-0207 [weitere DOIs]
    python3 scripts/crossref_lookup.py search "Titel der Arbeit" [--year 2007]
Ausgabe: JSON (eine Zeile pro Treffer). Prüft zusätzlich, ob Crossref Korrektur- oder
Rückzugsmitteilungen kennt, die auf die DOI verweisen (Filter `updates:`).

Grenzen: Crossref belegt Existenz und bibliografische Angaben, aber KEIN Peer Review
und keinen Inhalt. Fehlt ein Eintrag, heißt das nicht, dass die Quelle nicht existiert.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = 'https://api.crossref.org'
HEADERS = {'User-Agent': 'reyan232-research-assistant/1.0 (Seminar research metadata check)'}


def _get(url: str) -> dict:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:  # nutzt HTTPS_PROXY / SSL_CERT_FILE
        return json.load(resp)


def _year(item: dict) -> int | None:
    for key in ('published-print', 'published-online', 'issued', 'published'):
        parts = (item.get(key) or {}).get('date-parts') or [[None]]
        if parts and parts[0] and parts[0][0]:
            return int(parts[0][0])
    return None


def _authors(item: dict) -> str:
    names = []
    for a in item.get('author', []) or []:
        if a.get('family'):
            names.append(f"{a['family']}, {a.get('given', '').strip()}".rstrip(', '))
        elif a.get('name'):
            names.append(a['name'])
    return '; '.join(names)


def summarize(item: dict) -> dict:
    return {
        'doi': item.get('DOI', ''),
        'title': ' '.join(item.get('title') or []),
        'subtitle': ' '.join(item.get('subtitle') or []),
        'authors': _authors(item),
        'year': _year(item),
        'container': ' '.join(item.get('container-title') or []),
        'volume': item.get('volume', ''),
        'issue': item.get('issue', ''),
        'page': item.get('page', '') or item.get('article-number', ''),
        'type': item.get('type', ''),
        'publisher': item.get('publisher', ''),
        'isbn': '; '.join(item.get('ISBN') or []),
        'has_abstract': bool(item.get('abstract')),
        'url': f"https://doi.org/{item.get('DOI', '')}",
    }


def updates_for(doi: str) -> list[dict]:
    """Crossref-Mitteilungen (Korrektur, Rückzug, Expression of Concern), die diese DOI aktualisieren."""
    url = f"{API}/works?filter=updates:{urllib.parse.quote(doi)}&rows=20"
    items = _get(url).get('message', {}).get('items', [])
    out = []
    for it in items:
        for upd in it.get('update-to', []) or []:
            if upd.get('DOI', '').lower() == doi.lower():
                out.append({'type': upd.get('type', ''), 'notice_doi': it.get('DOI', '')})
    return out


def lookup_doi(doi: str) -> dict:
    doi = re.sub(r'^(https?://(dx\.)?doi\.org/|doi:)', '', doi.strip(), flags=re.I)
    try:
        item = _get(f"{API}/works/{urllib.parse.quote(doi)}")['message']
    except urllib.error.HTTPError as exc:
        return {'query_doi': doi, 'found': False, 'error': f'HTTP {exc.code}'}
    except Exception as exc:  # Netzwerk/Proxy
        return {'query_doi': doi, 'found': False, 'error': repr(exc)}
    result = {'query_doi': doi, 'found': True, **summarize(item)}
    try:
        result['updates'] = updates_for(item.get('DOI', doi))
    except Exception as exc:
        result['updates_error'] = repr(exc)
    return result


def search(title: str, year: int | None, rows: int = 5) -> list[dict]:
    params = {'query.bibliographic': title, 'rows': str(rows)}
    if year:
        params['filter'] = f'from-pub-date:{year - 1},until-pub-date:{year + 1}'
    url = f"{API}/works?{urllib.parse.urlencode(params)}"
    return [summarize(it) for it in _get(url).get('message', {}).get('items', [])]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    d = sub.add_parser('doi')
    d.add_argument('dois', nargs='+')
    s = sub.add_parser('search')
    s.add_argument('title')
    s.add_argument('--year', type=int)
    s.add_argument('--rows', type=int, default=5)
    args = ap.parse_args(argv)
    if args.cmd == 'doi':
        for doi in args.dois:
            print(json.dumps(lookup_doi(doi), ensure_ascii=False))
    else:
        for hit in search(args.title, args.year, args.rows):
            print(json.dumps(hit, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
