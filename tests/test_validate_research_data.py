import csv
import shutil
import tempfile
import unittest
from pathlib import Path
from scripts.validate_research_data import validate, BASE


class TestResearchDataValidation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for name in [
            '02_search/search_log.csv', '02_search/screening_log.csv',
            '03_sources/literature.csv', '03_sources/evidence_matrix.csv',
            '04_quality/benchmark_register.csv'
        ]:
            dst = self.root / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(BASE / name, dst)

    def tearDown(self):
        self.tmp.cleanup()

    def append(self, filename, record):
        with (self.root / filename).open('a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(record)

    def test_empty_initial_project_is_valid(self):
        self.assertEqual(validate(self.root), [])

    def test_unverified_article_cannot_be_included(self):
        self.append('03_sources/literature.csv', [
            'S001', 'Test title', 'A. Example', '2025', 'journal_article',
            'Journal X', '10.1111/example', '', '', '', 'NOT_CONFIRMED',
            'UNVERIFIED', 'ABSTRACT_ONLY', 'INCLUDED', '', ''
        ])
        findings = validate(self.root)
        self.assertTrue(any('Peer-Review' in msg for msg in findings))
        self.assertTrue(any('Metadaten' in msg for msg in findings))

    def test_claim_must_have_source(self):
        self.append('03_sources/evidence_matrix.csv', [
            'E1', 'S999', 'X', 'finding', 'page 5', 'FULL_TEXT', 'YES', 'high', '', ''
        ])
        findings = validate(self.root)
        self.assertTrue(any('unbekannte source_id' in msg for msg in findings))

    def test_grade_requires_external_proof(self):
        self.append('04_quality/benchmark_register.csv', [
            'B1', 'Beispiel', 'Bachelor', 'Uni X', '2024', '1.0', 'NO', '', '', 'structure', ''
        ])
        findings = validate(self.root)
        self.assertTrue(any('Note ohne externen Notennachweis' in msg for msg in findings))


if __name__ == '__main__':
    unittest.main()
