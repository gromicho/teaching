"""Catalogue entries must remain discoverable through the generated overview."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from update_notebook_overview import render


class NotebookOverviewTests(unittest.TestCase):
    def test_overview_matches_every_catalogued_notebook(self):
        catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
        overview = (ROOT / 'docs/NOTEBOOKS.md').read_text(encoding='utf-8')
        self.assertEqual(overview, render(catalog),
                         'Run python scripts/update_notebook_overview.py after changing the catalogue.')
        for item in catalog['notebooks']:
            self.assertEqual(overview.count(f"(../{item['path']})"), 1)
        self.assertIn('(docs/NOTEBOOKS.md)', (ROOT / 'README.md').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
