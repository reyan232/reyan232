"""Offline-Tests für scripts/crossref_lookup.py (kein Netzwerkzugriff)."""
import unittest

from scripts.crossref_lookup import summarize

# Erfundener, Crossref-ähnlicher Datensatz (DOI-Präfix 10.5555 = Crossref-Testpräfix)
ITEM = {
    'DOI': '10.5555/test-0001', 'title': ['Testtitel'], 'subtitle': ['Untertitel'],
    'author': [{'family': 'Muster', 'given': 'Max'}, {'name': 'Testkonsortium'}],
    'published-print': {'date-parts': [[2025, 3]]}, 'container-title': ['Testjournal'],
    'volume': '12', 'issue': '3', 'page': '1-20', 'type': 'journal-article',
    'publisher': 'Testverlag', 'abstract': '<jats:p>…</jats:p>',
}


class SummarizeTests(unittest.TestCase):
    def test_fields_are_extracted(self):
        s = summarize(ITEM)
        self.assertEqual(s['doi'], '10.5555/test-0001')
        self.assertEqual(s['authors'], 'Muster, Max; Testkonsortium')
        self.assertEqual(s['year'], 2025)
        self.assertEqual((s['container'], s['volume'], s['issue'], s['page']), ('Testjournal', '12', '3', '1-20'))
        self.assertTrue(s['has_abstract'])
        self.assertEqual(s['url'], 'https://doi.org/10.5555/test-0001')

    def test_missing_fields_do_not_crash(self):
        s = summarize({'DOI': '10.5555/x'})
        self.assertEqual((s['title'], s['authors'], s['year']), ('', '', None))
        self.assertFalse(s['has_abstract'])


if __name__ == '__main__':
    unittest.main()
