#!/usr/bin/env python3
"""Prüft CSV-Konsistenz; ersetzt keine wissenschaftliche Prüfung der Originaltexte."""
from __future__ import annotations
import csv
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REQUIRED = {
    '02_search/search_log.csv': {'search_id', 'search_date', 'database', 'search_string', 'result_count'},
    '02_search/screening_log.csv': {'source_id', 'title_abstract_decision', 'full_text_decision', 'exclusion_reason'},
    '03_sources/literature.csv': {'source_id', 'title', 'authors', 'year', 'source_type', 'doi', 'publication_url', 'peer_review_status', 'metadata_status', 'access_level', 'decision'},
    '03_sources/evidence_matrix.csv': {'evidence_id', 'source_id', 'claim_or_concept', 'source_location', 'verified_against_text'},
    '04_quality/benchmark_register.csv': {'benchmark_id', 'title', 'grade', 'grade_verified', 'grade_evidence_url'},
}
ALLOWED_TYPES = {'journal_article', 'peer_reviewed_conference', 'academic_book', 'academic_book_chapter', 'dissertation'}
PEER_REQUIRED = {'journal_article', 'peer_reviewed_conference'}
ACCESSES = {'NOT_ACCESSED', 'METADATA_ONLY', 'ABSTRACT_ONLY', 'FULL_TEXT'}


def load_csv(root: Path, name: str, errors: list[str]) -> list[dict]:
    path = root / name
    if not path.exists():
        errors.append(f'{name}: Datei fehlt')
        return []
    with path.open(encoding='utf-8-sig', newline='') as fh:
        rdr = csv.DictReader(fh)
        fields = set(rdr.fieldnames or [])
        missing = REQUIRED[name] - fields
        if missing:
            errors.append(f'{name}: Spalten fehlen: {", ".join(sorted(missing))}')
        rows = list(rdr)
        for ix, row in enumerate(rows, 2):
            if None in row:
                errors.append(f'{name}:{ix}: mehr Werte als Spalten')
        return rows


def validate(root: Path = BASE) -> list[str]:
    errors: list[str] = []
    data = {name: load_csv(root, name, errors) for name in REQUIRED}
    ids: set[str] = set()
    dois: set[str] = set()
    sources = data['03_sources/literature.csv']
    for row_no, r in enumerate(sources, 2):
        sid = (r.get('source_id') or '').strip()
        doi = (r.get('doi') or '').strip().lower().removeprefix('https://doi.org/')
        if not sid or sid in ids: errors.append(f'literature.csv:{row_no}: leere/duplizierte source_id')
        ids.add(sid)
        if doi:
            if doi in dois: errors.append(f'literature.csv:{row_no}: doppelte DOI')
            dois.add(doi)
            if not doi.startswith('10.'): errors.append(f'literature.csv:{row_no}: DOI sieht ungültig aus')
        kind = (r.get('source_type') or '').strip()
        if kind and kind not in ALLOWED_TYPES: errors.append(f'literature.csv:{row_no}: nicht zugelassener Publikationstyp {kind!r}')
        access = (r.get('access_level') or '').strip()
        if access and access not in ACCESSES: errors.append(f'literature.csv:{row_no}: ungültiger access_level')
        if (r.get('decision') or '').strip().upper() == 'INCLUDED':
            for field in ('title', 'authors', 'year', 'source_type', 'publication', 'metadata_status'):
                if not (r.get(field) or '').strip(): errors.append(f'literature.csv:{row_no}: INCLUDED ohne {field}')
            if (r.get('metadata_status') or '').strip().upper() != 'VERIFIED':
                errors.append(f'literature.csv:{row_no}: INCLUDED ohne verifizierte Metadaten')
            if kind in PEER_REQUIRED and (r.get('peer_review_status') or '').strip().upper() != 'CONFIRMED':
                errors.append(f'literature.csv:{row_no}: INCLUDED ohne Peer-Review-Nachweis')
            if not (doi or (r.get('isbn') or '').strip() or (r.get('urn') or '').strip() or (r.get('publication_url') or '').strip()):
                errors.append(f'literature.csv:{row_no}: INCLUDED ohne prüfbare Publikationskennung/URL')
    evidence_ids: set[str] = set()
    for row_no, r in enumerate(data['03_sources/evidence_matrix.csv'], 2):
        eid = (r.get('evidence_id') or '').strip()
        if not eid or eid in evidence_ids: errors.append(f'evidence_matrix.csv:{row_no}: leere/duplizierte evidence_id')
        evidence_ids.add(eid)
        sid = (r.get('source_id') or '').strip()
        if sid not in ids: errors.append(f'evidence_matrix.csv:{row_no}: unbekannte source_id {sid!r}')
        if (r.get('verified_against_text') or '').strip().upper() == 'YES':
            if not (r.get('source_location') or '').strip():
                errors.append(f'evidence_matrix.csv:{row_no}: YES ohne genaue Fundstelle')
            if (r.get('access_level') or '').strip().upper() != 'FULL_TEXT':
                errors.append(f'evidence_matrix.csv:{row_no}: YES ohne FULL_TEXT-Zugriff')
    for row_no, r in enumerate(data['04_quality/benchmark_register.csv'], 2):
        if (r.get('grade') or '').strip():
            if (r.get('grade_verified') or '').strip().upper() != 'YES' or not (r.get('grade_evidence_url') or '').strip():
                errors.append(f'benchmark_register.csv:{row_no}: Note ohne externen Notennachweis')
    return errors


if __name__ == '__main__':
    problems = validate()
    if problems:
        print(f'FEHLER ({len(problems)}):')
        for problem in problems: print('- ' + problem)
        sys.exit(1)
    print('OK: CSV-Struktur und basale Konsistenzregeln erfüllt. Kein Beweis für fachliche Richtigkeit.')
