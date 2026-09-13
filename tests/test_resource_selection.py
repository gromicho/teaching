"""A targeted execution must not hide malformed or unregistered notebooks."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import nbformat

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_resources


class ResourceSelectionTests(unittest.TestCase):
    def make_root(self, path):
        items = []
        for name in ['selected.ipynb', 'other.ipynb']:
            nb = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell('x = 1')])
            nbformat.write(nb, path / name)
            items.append({'path': name, 'kind': 'worked-example', 'execution_profile': 'core'})
        (path / 'catalog.json').write_text(json.dumps({
            'repository': 'gromicho/teaching', 'visibility': 'public', 'notebooks': items,
        }), encoding='utf-8')

    def test_selects_execution_but_keeps_structural_checks(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(check_resources, 'NotebookClient') as client:
            root = Path(tmp)
            self.make_root(root)
            report = check_resources.check(root, execute=True, notebooks=['selected.ipynb'])
            self.assertEqual(report['errors'], [])
            self.assertEqual([r['execution'] for r in report['results']], ['pass', 'not selected'])
            client.return_value.execute.assert_called_once()
            other = nbformat.read(root / 'other.ipynb', as_version=4)
            other.cells[0].execution_count = 1
            nbformat.write(other, root / 'other.ipynb')
            report = check_resources.check(root, execute=True, notebooks=['selected.ipynb'])
            self.assertTrue(any('other.ipynb' in error for error in report['errors']))

    def test_typo_cannot_report_an_empty_execution_success(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(check_resources, 'NotebookClient') as client:
            root = Path(tmp)
            self.make_root(root)
            report = check_resources.check(root, execute=True, notebooks=['typo.ipynb'])
            self.assertTrue(any('Unknown notebook' in error for error in report['errors']))
            client.assert_not_called()


if __name__ == '__main__':
    unittest.main()
