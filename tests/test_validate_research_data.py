"""Tests für die Forschungsdaten-Prüfungen.

Alle Testdatensätze sind ERFUNDENE Platzhalter (DOI-Präfix 10.5555 = Crossref-
Testpräfix) und dürfen niemals in die echten Projektdateien übernommen werden.
"""
import csv
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_research_data import (
    BASE, COLUMNS, KI_COLUMNS, KI_PROTOCOL, check_research_data, validate,
)

LIT = '03_sources/literature.csv'
EVI = '03_sources/evidence_matrix.csv'
SEARCH = '02_search/search_log.csv'
SCREEN = '02_search/screening_log.csv'
BENCH = '04_quality/benchmark_register.csv'

SEARCH_ROW = {
    'search_id': 'S001', 'search_date': '2026-11-07', 'executed_by': 'Student',
    'database': 'TESTDATENBANK', 'interface': 'Test', 'search_string': '"ai agent*" AND controlling',
    'filters': '2020-2026', 'result_count': '12', 'result_count_basis': 'DATENBANK_GESAMT',
}
VALID_SOURCE = {
    'source_id': 'Q001', 'title': 'Testtitel ohne reale Entsprechung', 'authors': 'Muster, Max',
    'year': '2025', 'source_type': 'ZEITSCHRIFTENARTIKEL', 'publication': 'Testjournal',
    'publisher': 'Testverlag', 'doi': '10.5555/test-0001',
    'peer_review_status': 'BESTAETIGT', 'peer_review_evidence': 'https://example.org/review-policy',
    'metadata_status': 'VERIFIZIERT', 'metadata_evidence': 'https://example.org/metadata',
    'access_level': 'VOLLTEXT_GELESEN', 'integrity_flags': 'KEINE_BEKANNT',
    'finance_area': 'CONTROLLING', 'found_via': 'S001', 'decision': 'AUFGENOMMEN',
    'added_by': 'Test', 'added_date': '2026-11-07',
}
VALID_EVIDENCE = {
    'evidence_id': 'E001', 'source_id': 'Q001', 'claim_or_finding': 'Testbefund',
    'theme': 'USE_CASE', 'finance_area': 'CONTROLLING', 'evidence_type': 'FALLSTUDIE',
    'source_location': 'S. 5, Tab. 2', 'access_level': 'VOLLTEXT_GELESEN',
    'verified_against_text': 'JA', 'reliability': 'MITTEL',
}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for name in list(COLUMNS) + ['03_sources/library.bib']:
            dst = self.root / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(BASE / name, dst)

    def tearDown(self):
        self.tmp.cleanup()

    def add(self, filename, record, columns=None):
        columns = columns or COLUMNS[filename]
        with (self.root / filename).open('a', newline='', encoding='utf-8') as fh:
            csv.DictWriter(fh, fieldnames=columns).writerow(record)

    def errors(self):
        return check_research_data(self.root).errors

    def assertFinding(self, needle, findings=None):
        findings = self.errors() if findings is None else findings
        self.assertTrue(any(needle in f for f in findings),
                        f'erwartet Meldung mit {needle!r}, erhalten: {findings}')


class TemplateTests(Base):
    def test_empty_templates_are_valid(self):
        self.assertEqual(validate(self.root), [])

    def test_repository_data_files_are_valid(self):
        self.assertEqual(check_research_data(BASE).errors, [])

    def test_missing_column_is_reported(self):
        path = self.root / LIT
        path.write_text('source_id,title\n', encoding='utf-8')
        self.assertFinding('Spalten fehlen')


class LiteratureGateTests(Base):
    def test_valid_included_article_passes(self):
        self.add(SEARCH, SEARCH_ROW)
        self.add(LIT, VALID_SOURCE)
        self.assertEqual(self.errors(), [])

    def test_unverified_article_cannot_be_included(self):
        self.add(SEARCH, SEARCH_ROW)
        self.add(LIT, {**VALID_SOURCE, 'peer_review_status': 'UNKLAR', 'peer_review_evidence': '',
                       'metadata_status': 'NICHT_VERIFIZIERT', 'metadata_evidence': ''})
        findings = self.errors()
        self.assertFinding('Peer-Review', findings)
        self.assertFinding('Metadaten', findings)

    def test_preprint_cannot_be_included(self):
        self.add(SEARCH, SEARCH_ROW)
        self.add(LIT, {**VALID_SOURCE, 'source_type': 'PREPRINT'})
        self.assertFinding('nicht zulässigem Publikationstyp')

    def test_preprint_can_be_documented_as_excluded(self):
        self.add(SEARCH, SEARCH_ROW)
        self.add(LIT, {**VALID_SOURCE, 'source_type': 'PREPRINT', 'decision': 'AUSGESCHLOSSEN',
                       'decision_reason': 'unbegutachteter Preprint'})
        self.assertEqual(self.errors(), [])

    def test_metadata_only_source_cannot_be_included(self):
        self.add(SEARCH, SEARCH_ROW)
        self.add(LIT, {**VALID_SOURCE, 'access_level': 'NUR_METADATA'})
        self.assertFinding('ohne inhaltliche Sichtung')

    def test_retracted_source_cannot_be_included(self):
        self.add(SEARCH, SEARCH_ROW)
        self.add(LIT, {**VALID_SOURCE, 'integrity_flags': 'ZURUECKGEZOGEN'})
        self.assertFinding('zurückgezogene Publikation')

    def test_invalid_doi_and_isbn_are_reported(self):
        self.add(SEARCH, SEARCH_ROW)
        self.add(LIT, {**VALID_SOURCE, 'doi': 'doi-erfunden', 'isbn': '978-3-16-148410-9'})
        findings = self.errors()
        self.assertFinding('DOI', findings)
        self.assertFinding('ISBN', findings)

    def test_valid_isbn_checksums_pass(self):
        self.add(SEARCH, SEARCH_ROW)
        self.add(LIT, {**VALID_SOURCE, 'source_type': 'FACHBUCH', 'doi': '',
                       'peer_review_status': 'NICHT_ZUTREFFEND', 'peer_review_evidence': '',
                       'isbn': '978-3-16-148410-0; 0-306-40615-2'})
        self.assertEqual(self.errors(), [])

    def test_duplicate_doi_is_reported(self):
        self.add(SEARCH, SEARCH_ROW)
        self.add(LIT, VALID_SOURCE)
        self.add(LIT, {**VALID_SOURCE, 'source_id': 'Q002', 'doi': 'https://doi.org/10.5555/TEST-0001'})
        self.assertFinding('doppelte DOI')

    def test_found_via_must_reference_logged_search(self):
        self.add(LIT, {**VALID_SOURCE, 'found_via': 'S999'})
        self.assertFinding("found_via='S999'")

    def test_unknown_vocabulary_is_reported(self):
        self.add(SEARCH, SEARCH_ROW)
        self.add(LIT, {**VALID_SOURCE, 'decision': 'INCLUDED'})
        self.assertFinding('decision=')

    def test_exclusion_requires_reason(self):
        self.add(LIT, {**VALID_SOURCE, 'found_via': 'STUDENT', 'decision': 'AUSGESCHLOSSEN'})
        self.assertFinding('ohne decision_reason')


class EvidenceTests(Base):
    def setUp(self):
        super().setUp()
        self.add(SEARCH, SEARCH_ROW)
        self.add(LIT, VALID_SOURCE)

    def test_valid_evidence_passes(self):
        self.add(EVI, VALID_EVIDENCE)
        self.assertEqual(self.errors(), [])

    def test_claim_must_have_known_source(self):
        self.add(EVI, {**VALID_EVIDENCE, 'source_id': 'Q999'})
        self.assertFinding('unbekannte source_id')

    def test_claim_requires_included_source(self):
        self.add(LIT, {**VALID_SOURCE, 'source_id': 'Q002', 'doi': '10.5555/test-0002',
                       'title': 'Zweiter Testtitel', 'decision': 'KANDIDAT'})
        self.add(EVI, {**VALID_EVIDENCE, 'source_id': 'Q002'})
        self.assertFinding('nicht AUFGENOMMEN')

    def test_verified_claim_requires_full_text(self):
        self.add(EVI, {**VALID_EVIDENCE, 'access_level': 'NUR_ABSTRACT', 'source_location': 'Abstract'})
        self.assertFinding('ohne VOLLTEXT_GELESEN')

    def test_page_reference_without_full_text_is_rejected(self):
        self.add(EVI, {**VALID_EVIDENCE, 'access_level': 'NUR_ABSTRACT',
                       'verified_against_text': 'TEILWEISE', 'source_location': 'S. 12'})
        self.assertFinding('Seitenangabe')

    def test_metadata_only_claim_is_rejected(self):
        self.add(EVI, {**VALID_EVIDENCE, 'access_level': 'NUR_METADATA',
                       'verified_against_text': 'NEIN', 'source_location': ''})
        self.assertFinding('Metadaten belegen keine Aussage')

    def test_evidence_access_cannot_exceed_literature_access(self):
        self.add(LIT, {**VALID_SOURCE, 'source_id': 'Q002', 'doi': '10.5555/test-0002',
                       'title': 'Zweiter Testtitel', 'access_level': 'NUR_ABSTRACT'})
        self.add(EVI, {**VALID_EVIDENCE, 'source_id': 'Q002'})
        self.assertFinding('höher als in literature.csv')


class SearchScreeningBenchmarkTests(Base):
    def test_estimated_result_count_is_rejected(self):
        self.add(SEARCH, {**SEARCH_ROW, 'result_count': 'ca. 50'})
        self.assertFinding('ganze Zahl')

    def test_search_requires_exact_string(self):
        self.add(SEARCH, {**SEARCH_ROW, 'search_string': ''})
        self.assertFinding('search_string fehlt')

    def test_screening_exclusion_requires_reason(self):
        self.add(SEARCH, SEARCH_ROW)
        self.add(SCREEN, {'source_id': 'Q010', 'search_id': 'S001', 'title': 'X',
                          'title_abstract_decision': 'AUSGESCHLOSSEN'})
        self.assertFinding('Ausschluss ohne exclusion_reason')

    def test_grade_requires_external_proof(self):
        self.add(BENCH, {'benchmark_id': 'B001', 'benchmark_type': 'ABSCHLUSSARBEIT',
                         'title': 'Beispiel', 'grade': '1,0', 'grade_verified': 'NEIN'})
        self.assertFinding('Note ohne externen Notennachweis')


class BibProvenanceProtocolTests(Base):
    def test_bib_key_requires_verified_source(self):
        with (self.root / '03_sources/library.bib').open('a', encoding='utf-8') as fh:
            fh.write('\n@article{Q404,\n  title = {Nicht registriert}\n}\n')
        self.assertFinding("Key 'Q404'")

    def test_bib_key_for_verified_source_passes(self):
        self.add(SEARCH, SEARCH_ROW)
        self.add(LIT, VALID_SOURCE)
        with (self.root / '03_sources/library.bib').open('a', encoding='utf-8') as fh:
            fh.write('\n@article{Q001,\n  title = {Testtitel ohne reale Entsprechung}\n}\n')
        self.assertEqual(self.errors(), [])

    def test_notes_require_provenance_line(self):
        notes = self.root / '05_research_notes'
        notes.mkdir(parents=True)
        (notes / 'notiz.md').write_text('# Notiz\nInhalt\n', encoding='utf-8')
        self.assertFinding('Herkunftszeile fehlt')
        (notes / 'notiz.md').write_text(
            '# Notiz\n> Herkunft: KI-generiert (source-researcher, 2026-11-07) – nicht zur Abgabe\n',
            encoding='utf-8')
        self.assertEqual(self.errors(), [])

    def test_missing_ki_protocol_is_only_a_warning(self):
        report = check_research_data(self.root)
        self.assertEqual(report.errors, [])
        self.assertTrue(any('ki_nutzungsprotokoll' in w for w in report.warnings))

    def test_ki_protocol_entries_are_checked(self):
        path = self.root / KI_PROTOCOL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(','.join(KI_COLUMNS) + '\n', encoding='utf-8')
        self.add(KI_PROTOCOL, {'datum': '07.11.2026', 'tool_agent': 'Test'}, columns=KI_COLUMNS)
        findings = self.errors()
        self.assertFinding('datum', findings)
        self.assertFinding('verwendungszweck fehlt', findings)


if __name__ == '__main__':
    unittest.main()
