#!/usr/bin/env python3
"""Lokale Qualitätschecks für das Forschungsprojekt „Finance AI Agents“.

Prüft Struktur und Konsistenz der Recherche-Dateien (CSV, BibTeX, Notiz-
Kennzeichnung) sowie die Projektstruktur (Agenten, Skills, Schutzregeln).
Ersetzt KEINE wissenschaftliche Prüfung der Originaltexte: ein grünes Ergebnis
heißt nur „formal konsistent“, nicht „fachlich richtig“.

Aufruf:
    python3 scripts/validate_research_data.py            # Daten + Struktur
    python3 scripts/validate_research_data.py --strict   # Hinweise zählen als Fehler
    python3 scripts/validate_research_data.py --root PFAD

Vokabular und Regeln: 00_admin/datenmodell.md
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# Spalten (Reihenfolge = Kopfzeile der Vorlagen)
# ---------------------------------------------------------------------------
COLUMNS: dict[str, list[str]] = {
    '03_sources/literature.csv': [
        'source_id', 'title', 'authors', 'year', 'source_type', 'publication', 'publisher',
        'volume_issue_pages', 'doi', 'isbn', 'urn', 'publication_url', 'peer_review_status',
        'peer_review_evidence', 'metadata_status', 'metadata_evidence', 'access_level',
        'integrity_flags', 'finance_area', 'found_via', 'decision', 'decision_reason',
        'added_by', 'added_date', 'notes'],
    '03_sources/evidence_matrix.csv': [
        'evidence_id', 'source_id', 'claim_or_finding', 'theme', 'finance_area', 'evidence_type',
        'source_location', 'access_level', 'verified_against_text', 'reliability', 'limitations',
        'related_evidence', 'recorded_by', 'recorded_date', 'notes'],
    '02_search/search_log.csv': [
        'search_id', 'search_date', 'executed_by', 'database', 'interface', 'search_string',
        'filters', 'result_count', 'result_count_basis', 'export_path', 'notes'],
    '02_search/screening_log.csv': [
        'source_id', 'search_id', 'title', 'title_abstract_decision', 'full_text_decision',
        'exclusion_code', 'exclusion_reason', 'reviewer', 'screening_date', 'notes'],
    '04_quality/benchmark_register.csv': [
        'benchmark_id', 'benchmark_type', 'title', 'degree_type', 'institution', 'year', 'grade',
        'grade_verified', 'grade_evidence_url', 'document_url', 'access_date',
        'quality_criterion', 'notes'],
}
KI_PROTOCOL = '00_admin/ki_nutzungsprotokoll.csv'
KI_COLUMNS = [
    'datum', 'tool_agent', 'phase_aufgabe', 'verwendungszweck', 'art_der_ausgabe',
    'vom_studenten_genutzt', 'originalquellen_geprueft', 'qualitaet_probleme',
    'menschliche_entscheidung', 'offene_fragen']

# ---------------------------------------------------------------------------
# Kontrolliertes Vokabular
# ---------------------------------------------------------------------------
ADMISSIBLE_TYPES = {'ZEITSCHRIFTENARTIKEL', 'KONFERENZBEITRAG', 'FACHBUCH',
                    'SAMMELBANDBEITRAG', 'DISSERTATION'}
NON_ADMISSIBLE_TYPES = {'PREPRINT', 'WORKING_PAPER', 'PRAXISBEITRAG', 'GRAUE_LITERATUR', 'SONSTIGES'}
PEER_REVIEW_REQUIRED = {'ZEITSCHRIFTENARTIKEL', 'KONFERENZBEITRAG'}
PEER_REVIEW = {'BESTAETIGT', 'NICHT_BESTAETIGT', 'NICHT_ZUTREFFEND', 'UNKLAR'}
METADATA = {'VERIFIZIERT', 'NICHT_VERIFIZIERT', 'WIDERSPRUECHLICH'}
ACCESS_ORDER = ['KEIN_ZUGRIFF', 'NUR_METADATA', 'NUR_ABSTRACT', 'VOLLTEXT_GELESEN']
ACCESS = set(ACCESS_ORDER)
INTEGRITY = {'KEINE_BEKANNT', 'ZURUECKGEZOGEN', 'KORRIGIERT', 'KONTROVERS'}
FINANCE_AREAS = {'CONTROLLING', 'ACCOUNTING', 'TREASURY', 'FINANZFUNKTION_UEBERGREIFEND',
                 'TECHNIK_GRUNDLAGEN', 'NICHT_ZIELBEREICH'}
DECISIONS = {'KANDIDAT', 'AUFGENOMMEN', 'AUFGENOMMEN_ERGAENZEND', 'AUSGESCHLOSSEN', 'ZURUECKGESTELLT'}
INCLUDED = {'AUFGENOMMEN', 'AUFGENOMMEN_ERGAENZEND'}
# Stufe 2 (Entscheidung K2 = B, 2026-11-07): nur Praxis-Fachzeitschriften, vorrangig
# aus der „Auswahl wissenschaftlicher Zeitschriften im Bereich Controlling/Finanzen“
# der Professorenvorgaben (Stand 10/2017, Anhang 4, S. 25). Normalisierte Schlüssel.
TIER2_TYPES = {'PRAXISBEITRAG'}
ANHANG4_JOURNALS = [
    'betriebs berater', 'betriebswirtschaftliche forschung und praxis', 'bfup', 'cfo aktuell',
    'magazine for chief financial officers', 'cfo magazine', 'controller magazin',
    'controlling management review', 'zeitschrift für erfolgsorientierte unternehmenssteuerung',
    'corporate finance', 'der betrieb', 'risk compliance audit', 'risiko manager',
    'zeitschrift für betriebswirtschaftliche forschung', 'zfbf',
    'zeitschrift für bilanzierung rechnungswesen und controlling',
    'zeitschrift für corporate governance', 'zeitschrift für das gesamte kreditwesen',
    'zeitschrift für internationale rechnungslegung',
]
TIER2_MAX_RELIABILITY = {'MITTEL', 'GERING', 'UNKLAR'}
FOUND_VIA_KEYWORDS = {'HINWEIS_DOZENT', 'STUDENT', 'SEMINARFOLIE'}
THEMES = {'TECHNIK_EINORDNUNG', 'USE_CASE', 'VERBREITUNG', 'NUTZEN_EFFIZIENZ',
          'NUTZEN_EFFEKTIVITAET', 'ERFOLGSFAKTOR', 'RISIKO_GRENZE', 'UMSETZUNG_PRAXIS',
          'METHODIK', 'SONSTIGES'}
EVIDENCE_TYPES = {'EMPIRISCH_QUANTITATIV', 'EMPIRISCH_QUALITATIV', 'FALLSTUDIE',
                  'EXPERIMENT_PROTOTYP', 'LITERATURREVIEW', 'KONZEPTIONELL', 'DEFINITION'}
VERIFIED = {'JA', 'TEILWEISE', 'NEIN'}
RELIABILITY = {'HOCH', 'MITTEL', 'GERING', 'UNKLAR'}
COUNT_BASIS = {'DATENBANK_GESAMT', 'ZURUECKGEGEBENE_TREFFER', 'UNBEKANNT'}
SCREENING = {'EINGESCHLOSSEN', 'AUSGESCHLOSSEN', 'UNKLAR'}
BENCHMARK_TYPES = {'HOCHSCHULRUBRIK', 'SCHREIBLEITFADEN', 'ABSCHLUSSARBEIT', 'SEMINARARBEIT',
                   'PREISGEKROENTE_ARBEIT', 'SONSTIGES'}
GRADE_VERIFIED = {'JA', 'NEIN', 'UNBEKANNT'}

DOI_RE = re.compile(r'^10\.\d{4,9}/\S+$')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
PAGE_RE = re.compile(r'(\bS\.|\bp\.|\bpp\.|\bSeite[n]?\b)\s*\d', re.IGNORECASE)
PROVENANCE_RE = re.compile(r'^\s*>?\s*Herkunft:\s*(KI-generiert|Student|gemischt)', re.IGNORECASE)
PROVENANCE_DIRS = ['05_research_notes', '07_feedback', '04_quality/reports']

# ---------------------------------------------------------------------------
# Projektstruktur
# ---------------------------------------------------------------------------
EXPECTED_AGENTS = ['source-researcher', 'quality-controller', 'scientific-critic',
                   'citation-auditor', 'methodology-advisor', 'finance-ai-expert']
EXPECTED_SKILLS = ['academic-excellence', 'academic-source-gate', 'review-protocol',
                   'citation-audit', 'critical-feedback', 'university-policy-check',
                   'seminar-deliverables']
AGENT_ALLOWED_TOOLS = {'Read', 'Glob', 'Grep', 'WebSearch', 'WebFetch'}
AGENT_SECTIONS = ['## Mission', '## Eingaben', '## Arbeitsschritte', '## Verbote',
                  '## Ergebnisvertrag', '## Übergabe an den Orchestrator']
SKILL_NAME_RE = re.compile(r'^[a-z0-9-]{1,64}$')
REQUIRED_FILES = [
    'CLAUDE.md', 'README.md', '.gitignore', '.claude/settings.json',
    '00_admin/hochschulregeln/README.md', '00_admin/compliance_status.md',
    '00_admin/seminar_requirements.md', '00_admin/requirements_checklist.md',
    '00_admin/decision_log.md', '00_admin/datenmodell.md',
    '00_admin/ki_nutzungsprotokoll.vorlage.csv',
    '01_scope/topic_options.md', '01_scope/research_question.md',
    '02_search/search_protocol.md', '03_sources/library.bib', '03_sources/pdfs/README.md',
    '04_quality/quality_rubric.md', '05_research_notes/README.md',
    '06_student_draft/README.md', '07_feedback/README.md',
]
GITIGNORE_MUST_CONTAIN = [
    '00_admin/hochschulregeln/*', '03_sources/pdfs/*', '06_student_draft/*',
    '.claude/settings.local.json', '00_admin/ki_nutzungsprotokoll.csv',
]


class Report:
    """Sammelt Fehler (blockierend) und Hinweise (nicht blockierend)."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------
def _v(row: dict, key: str) -> str:
    return (row.get(key) or '').strip()


def _short(name: str) -> str:
    return name.split('/')[-1]


def _valid_date(value: str) -> bool:
    if not DATE_RE.match(value):
        return False
    try:
        _dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _isbn_ok(raw: str) -> bool:
    s = re.sub(r'[\s-]', '', raw).upper()
    if len(s) == 10 and re.fullmatch(r'\d{9}[\dX]', s):
        total = sum((10 - i) * (10 if c == 'X' else int(c)) for i, c in enumerate(s))
        return total % 11 == 0
    if len(s) == 13 and s.isdigit():
        total = sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(s))
        return total % 10 == 0
    return False


def _norm_doi(raw: str) -> str:
    d = raw.strip().lower()
    for prefix in ('https://doi.org/', 'http://doi.org/', 'https://dx.doi.org/', 'doi:'):
        if d.startswith(prefix):
            d = d[len(prefix):]
    return d


def _check_vocab(rep: Report, where: str, field: str, value: str, allowed: set[str],
                 multi: bool = False) -> None:
    if not value:
        return
    values = [x.strip() for x in value.split(';')] if multi else [value]
    for item in values:
        if item not in allowed:
            rep.err(f'{where}: {field}={item!r} unzulässig. Erlaubt: {", ".join(sorted(allowed))}')


def load_csv(root: Path, name: str, columns: list[str], rep: Report,
             required: bool = True) -> list[dict] | None:
    path = root / name
    if not path.exists():
        if required:
            rep.err(f'{name}: Datei fehlt (Vorlage siehe 00_admin/datenmodell.md)')
        return None
    with path.open(encoding='utf-8-sig', newline='') as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        missing = [c for c in columns if c not in header]
        extra = [c for c in header if c not in columns]
        if missing:
            rep.err(f'{name}: Spalten fehlen: {", ".join(missing)}')
        if extra:
            rep.err(f'{name}: unbekannte Spalten: {", ".join(extra)} '
                    '(neue Spalten nur nach Freigabe + Validator-Anpassung)')
        if not missing and not extra and header != columns:
            rep.warn(f'{name}: Spaltenreihenfolge weicht von der Vorlage ab')
        rows = []
        for line_no, row in enumerate(reader, 2):
            if None in row:
                rep.err(f'{name}:{line_no}: mehr Werte als Spalten (Komma im Text? Feld in "…" setzen)')
            if not any((v or '').strip() for k, v in row.items() if k is not None):
                rep.warn(f'{name}:{line_no}: leere Zeile')
                continue
            row['_line'] = line_no
            rows.append(row)
        return rows


# ---------------------------------------------------------------------------
# Prüfungen Forschungsdaten
# ---------------------------------------------------------------------------
def _check_search_log(rows: list[dict], rep: Report) -> set[str]:
    ids: set[str] = set()
    for r in rows:
        w = f'search_log.csv:{r["_line"]}'
        sid = _v(r, 'search_id')
        if not sid or sid in ids:
            rep.err(f'{w}: leere oder doppelte search_id')
        ids.add(sid)
        if not _valid_date(_v(r, 'search_date')):
            rep.err(f'{w}: search_date fehlt oder nicht im Format JJJJ-MM-TT')
        for field in ('executed_by', 'database', 'search_string'):
            if not _v(r, field):
                rep.err(f'{w}: {field} fehlt (exakter Suchlauf muss reproduzierbar sein)')
        count = _v(r, 'result_count')
        basis = _v(r, 'result_count_basis')
        _check_vocab(rep, w, 'result_count_basis', basis, COUNT_BASIS)
        if count:
            if not count.isdigit():
                rep.err(f'{w}: result_count muss ganze Zahl sein oder leer bleiben (nie schätzen)')
            if not basis:
                rep.err(f'{w}: result_count ohne result_count_basis')
    return ids


def _check_literature(rows: list[dict], search_ids: set[str], rep: Report) -> dict[str, dict]:
    sources: dict[str, dict] = {}
    dois: dict[str, str] = {}
    title_keys: dict[tuple[str, str], str] = {}
    this_year = _dt.date.today().year
    for r in rows:
        w = f'literature.csv:{r["_line"]}'
        sid = _v(r, 'source_id')
        if not sid or sid in sources:
            rep.err(f'{w}: leere oder doppelte source_id')
        sources[sid] = r
        kind = _v(r, 'source_type')
        decision = _v(r, 'decision')
        _check_vocab(rep, w, 'source_type', kind, ADMISSIBLE_TYPES | NON_ADMISSIBLE_TYPES)
        _check_vocab(rep, w, 'peer_review_status', _v(r, 'peer_review_status'), PEER_REVIEW)
        _check_vocab(rep, w, 'metadata_status', _v(r, 'metadata_status'), METADATA)
        _check_vocab(rep, w, 'access_level', _v(r, 'access_level'), ACCESS)
        _check_vocab(rep, w, 'integrity_flags', _v(r, 'integrity_flags'), INTEGRITY, multi=True)
        _check_vocab(rep, w, 'finance_area', _v(r, 'finance_area'), FINANCE_AREAS, multi=True)
        _check_vocab(rep, w, 'decision', decision, DECISIONS)
        if not decision:
            rep.err(f'{w}: decision fehlt (KANDIDAT, AUFGENOMMEN, AUFGENOMMEN_ERGAENZEND, '
                    'AUSGESCHLOSSEN, ZURUECKGESTELLT)')

        year = _v(r, 'year')
        if year and not (year.isdigit() and len(year) == 4 and 1900 <= int(year) <= this_year + 1):
            rep.err(f'{w}: year={year!r} unplausibel (vierstellig, 1900–{this_year + 1})')
        if _v(r, 'added_date') and not _valid_date(_v(r, 'added_date')):
            rep.err(f'{w}: added_date nicht im Format JJJJ-MM-TT')

        doi = _norm_doi(_v(r, 'doi'))
        if doi:
            if not DOI_RE.match(doi):
                rep.err(f'{w}: DOI {doi!r} formal ungültig (erwartet 10.xxxx/…) – nie erfinden')
            if doi in dois:
                rep.err(f'{w}: doppelte DOI (bereits bei {dois[doi]}) – Dublette prüfen')
            dois[doi] = sid
        for isbn in filter(None, (x.strip() for x in _v(r, 'isbn').split(';'))):
            if not _isbn_ok(isbn):
                rep.err(f'{w}: ISBN {isbn!r} hat ungültige Prüfziffer/Länge – an Verlags-/Katalogdaten prüfen')
        title_key = (re.sub(r'\W+', ' ', _v(r, 'title').lower()).strip(), year)
        if title_key[0]:
            if title_key in title_keys:
                rep.warn(f'{w}: Titel+Jahr wie {title_keys[title_key]} – mögliche Dublette')
            title_keys[title_key] = sid

        found = [x.strip() for x in _v(r, 'found_via').split(';') if x.strip()]
        for token in found:
            if token in FOUND_VIA_KEYWORDS or token.startswith('SCHNEEBALL:'):
                continue
            if token not in search_ids:
                rep.err(f'{w}: found_via={token!r} ist weder search_id aus search_log.csv '
                        f'noch {", ".join(sorted(FOUND_VIA_KEYWORDS))} / SCHNEEBALL:<id>')

        if decision in {'AUSGESCHLOSSEN', 'ZURUECKGESTELLT'} and not _v(r, 'decision_reason'):
            rep.err(f'{w}: {decision} ohne decision_reason')

        if decision == 'AUFGENOMMEN':
            _check_inclusion_gate(r, w, kind, doi, found, rep)
        elif decision == 'AUFGENOMMEN_ERGAENZEND':
            _check_tier2_gate(r, w, kind, doi, found, rep)
    return sources


def _norm_text(value: str) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'[^\w]+', ' ', value.lower())).strip()


def is_anhang4_journal(publication: str) -> bool:
    norm = _norm_text(publication)
    return bool(norm) and any(key in norm for key in ANHANG4_JOURNALS)


def _check_common_inclusion(r: dict, w: str, doi: str, found: list[str], rep: Report, label: str) -> None:
    for field in ('title', 'year', 'publication'):
        if not _v(r, field):
            rep.err(f'{w}: {label} ohne {field}')
    if not _v(r, 'authors'):
        rep.err(f'{w}: {label} ohne authors (bei fehlender Verfasserangabe „o. V.“ eintragen)')
    if _v(r, 'metadata_status') != 'VERIFIZIERT':
        rep.err(f'{w}: {label} ohne verifizierte Metadaten (metadata_status=VERIFIZIERT)')
    if not _v(r, 'metadata_evidence'):
        rep.err(f'{w}: {label} ohne metadata_evidence (mind. ein zuverlässiger Metadatennachweis)')
    if not (doi or _v(r, 'isbn') or _v(r, 'urn') or _v(r, 'publication_url')):
        rep.err(f'{w}: {label} ohne prüfbare Kennung (DOI/ISBN/URN/URL)')
    if 'ZURUECKGEZOGEN' in _v(r, 'integrity_flags'):
        rep.err(f'{w}: zurückgezogene Publikation darf nicht {label} sein')
    access = _v(r, 'access_level')
    if access in {'', 'KEIN_ZUGRIFF', 'NUR_METADATA'}:
        rep.err(f'{w}: {label} ohne inhaltliche Sichtung (mind. NUR_ABSTRACT)')
    elif access == 'NUR_ABSTRACT':
        rep.warn(f'{w}: nur Abstract gesichtet – keine Detailaussagen/Seitenangaben ableiten; '
                 'Volltext (ggf. Fernleihe, Folie 72) beschaffen')
    if not found:
        rep.err(f'{w}: {label} ohne found_via (Rückverfolgbarkeit zur Suche)')
    if not _v(r, 'integrity_flags'):
        rep.warn(f'{w}: integrity_flags leer – Retraction/Korrektur noch nicht geprüft')


def _check_tier2_gate(r: dict, w: str, kind: str, doi: str, found: list[str], rep: Report) -> None:
    label = 'AUFGENOMMEN_ERGAENZEND'
    if kind not in TIER2_TYPES:
        rep.err(f'{w}: {label} nur für Praxis-Fachzeitschriften (source_type=PRAXISBEITRAG); '
                f'{kind!r} ist '
                + ('Stufe 1 → AUFGENOMMEN verwenden' if kind in ADMISSIBLE_TYPES
                   else 'weiterhin ausgeschlossen (Preprint, Working Paper, graue Literatur …)'))
    _check_common_inclusion(r, w, doi, found, rep, label)
    if not _v(r, 'decision_reason'):
        rep.err(f'{w}: {label} ohne decision_reason (Begründung inkl. CRAAP-Prüfung)')
    if not is_anhang4_journal(_v(r, 'publication')):
        rep.warn(f'{w}: {_v(r, "publication")!r} steht nicht in Anhang 4 der Professorenvorgaben – '
                 'Einzelfreigabe des Studenten im decision_log erforderlich')


def _check_inclusion_gate(r: dict, w: str, kind: str, doi: str, found: list[str], rep: Report) -> None:
    if kind in TIER2_TYPES:
        rep.err(f'{w}: Praxisbeitrag ist Stufe 2 → AUFGENOMMEN_ERGAENZEND statt AUFGENOMMEN verwenden')
    elif kind not in ADMISSIBLE_TYPES:
        rep.err(f'{w}: AUFGENOMMEN mit nicht zulässigem Publikationstyp {kind!r} '
                '(nur peer-review. Zeitschrift/Konferenz, Fachbuch, Sammelband, Dissertation)')
    _check_common_inclusion(r, w, doi, found, rep, 'AUFGENOMMEN')
    if kind in PEER_REVIEW_REQUIRED:
        if _v(r, 'peer_review_status') != 'BESTAETIGT':
            rep.err(f'{w}: AUFGENOMMEN ohne Peer-Review-Nachweis (peer_review_status=BESTAETIGT)')
        if not _v(r, 'peer_review_evidence'):
            rep.err(f'{w}: AUFGENOMMEN ohne peer_review_evidence (DOI allein belegt kein Peer Review)')


def _check_evidence(rows: list[dict], sources: dict[str, dict], rep: Report) -> None:
    ids: set[str] = set()
    for r in rows:
        w = f'evidence_matrix.csv:{r["_line"]}'
        eid = _v(r, 'evidence_id')
        if not eid or eid in ids:
            rep.err(f'{w}: leere oder doppelte evidence_id')
        ids.add(eid)
        sid = _v(r, 'source_id')
        src = sources.get(sid)
        if src is None:
            rep.err(f'{w}: unbekannte source_id {sid!r} (erst in literature.csv erfassen)')
        elif _v(src, 'decision') not in INCLUDED:
            rep.err(f'{w}: Quelle {sid} ist nicht AUFGENOMMEN – nicht verifizierte Quellen '
                    'gehören nicht in die Evidenzmatrix')
        elif _v(src, 'decision') == 'AUFGENOMMEN_ERGAENZEND':
            if _v(r, 'reliability') not in TIER2_MAX_RELIABILITY:
                rep.err(f'{w}: Stufe-2-Quelle {sid} (Praxisbeitrag) – reliability höchstens MITTEL')
            if not _v(r, 'limitations'):
                rep.err(f'{w}: Stufe-2-Quelle {sid} – limitations Pflicht (Praxisperspektive, '
                        'kein alleiniger Beleg für verallgemeinernde/empirische Aussagen)')
        if not _v(r, 'claim_or_finding'):
            rep.err(f'{w}: claim_or_finding fehlt')
        _check_vocab(rep, w, 'theme', _v(r, 'theme'), THEMES)
        _check_vocab(rep, w, 'finance_area', _v(r, 'finance_area'), FINANCE_AREAS, multi=True)
        _check_vocab(rep, w, 'evidence_type', _v(r, 'evidence_type'), EVIDENCE_TYPES)
        _check_vocab(rep, w, 'verified_against_text', _v(r, 'verified_against_text'), VERIFIED)
        _check_vocab(rep, w, 'reliability', _v(r, 'reliability'), RELIABILITY)
        access = _v(r, 'access_level')
        _check_vocab(rep, w, 'access_level', access, ACCESS)
        for field in ('theme', 'evidence_type', 'access_level', 'verified_against_text', 'reliability'):
            if not _v(r, field):
                rep.err(f'{w}: {field} fehlt')
        if access in {'KEIN_ZUGRIFF', 'NUR_METADATA'}:
            rep.err(f'{w}: Befund auf Basis von {access} unzulässig – Metadaten belegen keine Aussage')
        if src is not None and access in ACCESS and _v(src, 'access_level') in ACCESS:
            if ACCESS_ORDER.index(access) > ACCESS_ORDER.index(_v(src, 'access_level')):
                rep.err(f'{w}: access_level {access} höher als in literature.csv '
                        f'({_v(src, "access_level")}) – widersprüchlich')
        location = _v(r, 'source_location')
        verified = _v(r, 'verified_against_text')
        if verified == 'JA':
            if not location:
                rep.err(f'{w}: verified_against_text=JA ohne genaue Fundstelle')
            if access != 'VOLLTEXT_GELESEN':
                rep.err(f'{w}: verified_against_text=JA ohne VOLLTEXT_GELESEN')
        if location and PAGE_RE.search(location) and access != 'VOLLTEXT_GELESEN':
            rep.err(f'{w}: Seitenangabe {location!r} ohne Volltextsichtung – nicht zulässig')


def _check_screening(rows: list[dict], search_ids: set[str], sources: dict[str, dict],
                     rep: Report) -> None:
    seen: set[str] = set()
    for r in rows:
        w = f'screening_log.csv:{r["_line"]}'
        sid = _v(r, 'source_id')
        if not sid or sid in seen:
            rep.err(f'{w}: leere oder doppelte source_id')
        seen.add(sid)
        srch = _v(r, 'search_id')
        if srch and srch not in search_ids:
            rep.err(f'{w}: search_id {srch!r} nicht in search_log.csv')
        ta, ft = _v(r, 'title_abstract_decision'), _v(r, 'full_text_decision')
        _check_vocab(rep, w, 'title_abstract_decision', ta, SCREENING)
        _check_vocab(rep, w, 'full_text_decision', ft, SCREENING)
        if 'AUSGESCHLOSSEN' in (ta, ft) and not _v(r, 'exclusion_reason'):
            rep.err(f'{w}: Ausschluss ohne exclusion_reason')
        if ft and ta == 'AUSGESCHLOSSEN':
            rep.err(f'{w}: Volltext-Entscheidung trotz Ausschluss im Titel/Abstract-Screening')
        if _v(r, 'screening_date') and not _valid_date(_v(r, 'screening_date')):
            rep.err(f'{w}: screening_date nicht im Format JJJJ-MM-TT')
        src = sources.get(sid)
        if src is not None and _v(src, 'decision') in INCLUDED and 'AUSGESCHLOSSEN' in (ta, ft):
            rep.err(f'{w}: {sid} im Screening ausgeschlossen, in literature.csv aber AUFGENOMMEN')


def _check_benchmarks(rows: list[dict], rep: Report) -> None:
    ids: set[str] = set()
    for r in rows:
        w = f'benchmark_register.csv:{r["_line"]}'
        bid = _v(r, 'benchmark_id')
        if not bid or bid in ids:
            rep.err(f'{w}: leere oder doppelte benchmark_id')
        ids.add(bid)
        _check_vocab(rep, w, 'benchmark_type', _v(r, 'benchmark_type'), BENCHMARK_TYPES)
        _check_vocab(rep, w, 'grade_verified', _v(r, 'grade_verified'), GRADE_VERIFIED)
        if _v(r, 'grade') and (_v(r, 'grade_verified') != 'JA' or not _v(r, 'grade_evidence_url')):
            rep.err(f'{w}: Note ohne externen Notennachweis (grade_verified=JA + grade_evidence_url) '
                    '– sonst Feld grade leer lassen')
        if _v(r, 'grade_verified') == 'JA' and not _v(r, 'grade_evidence_url'):
            rep.err(f'{w}: grade_verified=JA ohne grade_evidence_url')


def _check_ki_protocol(root: Path, rep: Report) -> None:
    rows = load_csv(root, KI_PROTOCOL, KI_COLUMNS, rep, required=False)
    if rows is None:
        rep.warn(f'{KI_PROTOCOL} fehlt lokal (absichtlich nicht in Git). Aus '
                 '00_admin/ki_nutzungsprotokoll.vorlage.csv kopieren und jede KI-Nutzung eintragen.')
        return
    for r in rows:
        w = f'ki_nutzungsprotokoll.csv:{r["_line"]}'
        if not _valid_date(_v(r, 'datum')):
            rep.err(f'{w}: datum fehlt oder nicht im Format JJJJ-MM-TT')
        for field in ('tool_agent', 'verwendungszweck', 'qualitaet_probleme'):
            if not _v(r, field):
                rep.err(f'{w}: {field} fehlt (für Kolloquium-Folie zu KI-Tools nötig, Folie 56)')


def _check_bib(root: Path, sources: dict[str, dict], rep: Report) -> None:
    path = root / '03_sources/library.bib'
    if not path.exists():
        rep.err('03_sources/library.bib: Datei fehlt')
        return
    text = path.read_text(encoding='utf-8')
    keys = re.findall(r'^\s*@(\w+)\s*\{\s*([^,\s]+)\s*,', text, flags=re.MULTILINE)
    seen: set[str] = set()
    for entry_type, key in keys:
        if entry_type.lower() in {'comment', 'string', 'preamble'}:
            continue
        if key in seen:
            rep.err(f'library.bib: doppelter Key {key!r}')
        seen.add(key)
        src = sources.get(key)
        if src is None:
            rep.err(f'library.bib: Key {key!r} hat keine source_id in literature.csv')
        elif _v(src, 'metadata_status') != 'VERIFIZIERT':
            rep.err(f'library.bib: {key} steht in der Bibliografie, Metadaten aber nicht VERIFIZIERT')


def _check_provenance(root: Path, rep: Report) -> None:
    for folder in PROVENANCE_DIRS:
        base = root / folder
        if not base.exists():
            continue
        for md in sorted(base.rglob('*.md')):
            if md.name.lower() == 'readme.md':
                continue
            head = md.read_text(encoding='utf-8', errors='replace').splitlines()[:10]
            if not any(PROVENANCE_RE.match(line) for line in head):
                rel = md.relative_to(root).as_posix()
                rep.err(f'{rel}: Herkunftszeile fehlt (erste 10 Zeilen: '
                        '"> Herkunft: KI-generiert (…) – nicht zur Abgabe" oder "> Herkunft: Student")')


def check_research_data(root: Path = BASE) -> Report:
    rep = Report()
    data = {name: load_csv(root, name, cols, rep) or [] for name, cols in COLUMNS.items()}
    search_ids = _check_search_log(data['02_search/search_log.csv'], rep)
    sources = _check_literature(data['03_sources/literature.csv'], search_ids, rep)
    _check_evidence(data['03_sources/evidence_matrix.csv'], sources, rep)
    _check_screening(data['02_search/screening_log.csv'], search_ids, sources, rep)
    _check_benchmarks(data['04_quality/benchmark_register.csv'], rep)
    _check_ki_protocol(root, rep)
    _check_bib(root, sources, rep)
    _check_provenance(root, rep)
    return rep


# ---------------------------------------------------------------------------
# Prüfungen Projektstruktur (Agenten, Skills, Schutzregeln)
# ---------------------------------------------------------------------------
def parse_frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    """Gibt (frontmatter, body, fehlertext) zurück. Nutzt PyYAML, falls installiert."""
    if not text.startswith('---'):
        return None, text, 'YAML-Frontmatter fehlt (Datei muss mit --- beginnen)'
    parts = text.split('\n---', 1)
    if len(parts) != 2:
        return None, text, 'YAML-Frontmatter nicht mit --- abgeschlossen'
    raw = parts[0][3:].strip('\n')
    body = parts[1].split('\n', 1)[1] if '\n' in parts[1] else ''
    try:
        import yaml  # type: ignore
    except ImportError:  # einfacher Fallback ohne Abhängigkeit
        data: dict = {}
        for line in raw.splitlines():
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            if ':' not in line:
                return None, body, f'Zeile ohne "key: value": {line!r}'
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip().strip('"\'')
        return data, body, None
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return None, body, f'YAML ungültig: {exc}'
    if not isinstance(data, dict):
        return None, body, 'YAML-Frontmatter ist kein Mapping'
    return data, body, None


def _tools_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(t).strip() for t in value]
    return [t.strip() for t in str(value or '').split(',') if t.strip()]


def check_project_structure(root: Path = BASE) -> Report:
    rep = Report()
    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            rep.err(f'{rel}: Pflichtdatei fehlt')

    agent_dir = root / '.claude/agents'
    found_agents = sorted(p.stem for p in agent_dir.glob('*.md')) if agent_dir.exists() else []
    for name in EXPECTED_AGENTS:
        path = agent_dir / f'{name}.md'
        if not path.exists():
            rep.err(f'.claude/agents/{name}.md: Agent fehlt')
            continue
        fm, body, problem = parse_frontmatter(path.read_text(encoding='utf-8'))
        where = f'.claude/agents/{name}.md'
        if problem:
            rep.err(f'{where}: {problem}')
            continue
        if fm.get('name') != name:
            rep.err(f'{where}: name={fm.get("name")!r} passt nicht zum Dateinamen')
        if not str(fm.get('description') or '').strip():
            rep.err(f'{where}: description fehlt')
        tools = _tools_list(fm.get('tools'))
        if not tools:
            rep.err(f'{where}: tools fehlt (Subagents sollen nur lesen/recherchieren)')
        forbidden = [t for t in tools if t not in AGENT_ALLOWED_TOOLS]
        if forbidden:
            rep.err(f'{where}: nicht erlaubte Tools {forbidden} – Subagents dürfen nicht schreiben/ausführen')
        for section in AGENT_SECTIONS:
            if section not in body:
                rep.err(f'{where}: Abschnitt "{section}" fehlt')
    for extra in sorted(set(found_agents) - set(EXPECTED_AGENTS)):
        rep.warn(f'.claude/agents/{extra}.md: zusätzlicher, nicht dokumentierter Agent')

    skill_dir = root / '.claude/skills'
    for name in EXPECTED_SKILLS:
        path = skill_dir / name / 'SKILL.md'
        where = f'.claude/skills/{name}/SKILL.md'
        if not path.exists():
            rep.err(f'{where}: Skill fehlt')
            continue
        fm, body, problem = parse_frontmatter(path.read_text(encoding='utf-8'))
        if problem:
            rep.err(f'{where}: {problem}')
            continue
        if fm.get('name') != name or not SKILL_NAME_RE.match(str(fm.get('name'))):
            rep.err(f'{where}: name={fm.get("name")!r} muss dem Ordnernamen entsprechen (a-z, 0-9, -)')
        desc = str(fm.get('description') or '').strip()
        if not desc:
            rep.err(f'{where}: description fehlt')
        elif len(desc) > 1024:
            rep.err(f'{where}: description länger als 1024 Zeichen')
        if 'Beispiel' not in body:
            rep.err(f'{where}: Beispielnutzung fehlt')

    settings = root / '.claude/settings.json'
    if settings.exists():
        try:
            cfg = json.loads(settings.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            rep.err(f'.claude/settings.json: ungültiges JSON: {exc}')
        else:
            deny = (cfg.get('permissions') or {}).get('deny') or []
            if not any(r.startswith('Edit(') and '06_student_draft' in r for r in deny):
                rep.err('.claude/settings.json: Schreibschutz für 06_student_draft/ fehlt '
                        '(permissions.deny mit Edit(...06_student_draft/**))')

    gitignore = root / '.gitignore'
    if gitignore.exists():
        lines = {ln.strip() for ln in gitignore.read_text(encoding='utf-8').splitlines()}
        for pattern in GITIGNORE_MUST_CONTAIN:
            if pattern not in lines:
                rep.err(f'.gitignore: Schutzregel {pattern!r} fehlt')
    return rep


# ---------------------------------------------------------------------------
# Rückwärtskompatible Kurzform + CLI
# ---------------------------------------------------------------------------
def validate(root: Path = BASE) -> list[str]:
    """Nur blockierende Fehler der Forschungsdaten (Kompatibilität mit Starter-Tests)."""
    return check_research_data(root).errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--root', type=Path, default=BASE, help='Projektwurzel (Standard: Repo)')
    parser.add_argument('--strict', action='store_true', help='Hinweise ebenfalls als Fehler werten')
    parser.add_argument('--data-only', action='store_true', help='nur Forschungsdaten prüfen')
    args = parser.parse_args(argv)

    data = check_research_data(args.root)
    errors, warnings = list(data.errors), list(data.warnings)
    if not args.data_only:
        struct = check_project_structure(args.root)
        errors += struct.errors
        warnings += struct.warnings

    if warnings:
        print(f'HINWEISE ({len(warnings)}):')
        for w in warnings:
            print('  - ' + w)
    if errors:
        print(f'FEHLER ({len(errors)}):')
        for e in errors:
            print('  - ' + e)
        print('Ergebnis: NICHT BESTANDEN. Bitte Fehler beheben; Vokabular in 00_admin/datenmodell.md.')
        return 1
    if args.strict and warnings:
        print('Ergebnis: NICHT BESTANDEN (--strict: Hinweise zählen als Fehler).')
        return 1
    print('OK: Struktur und Konsistenzregeln erfüllt. Kein Beweis für fachliche Richtigkeit.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
