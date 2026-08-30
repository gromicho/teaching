"""Run every maintained dependency cell with mocked package discovery/pip.

Set TEACHING_NOTEBOOK_ROOT to check the private collection with the same tests.
No packages are installed by these tests.
"""
import ast
import json
import os
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch

ROOT = Path(os.environ.get('TEACHING_NOTEBOOK_ROOT', Path(__file__).resolve().parents[1])).resolve()


def cells():
    catalog = json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))
    for item in catalog['notebooks']:
        if item['execution_profile'] == 'archive':
            continue
        notebook = json.loads((ROOT/item['path']).read_text(encoding='utf-8'))
        for cell in notebook['cells']:
            yield item['path'], cell, ''.join(cell['source'])


class SetupTests(unittest.TestCase):
    def test_no_unconditional_pip_or_version_pins(self):
        for path, cell, source in cells():
            if cell['cell_type'] == 'code':
                with self.subTest(path=path, cell=cell['id']):
                    self.assertFalse(re.search(r'^\s*[%!]pip\s', source, re.MULTILINE))
                    if 'package-install' in cell['metadata'].get('tags', []):
                        self.assertNotIn('==', source)
                        self.assertNotIn('--upgrade', source)

    def test_installed_packages_are_left_alone(self):
        checked = 0
        for path, cell, source in cells():
            if 'package-install' not in cell['metadata'].get('tags', []):
                continue
            checked += 1
            with self.subTest(path=path, cell=cell['id']), \
                    patch('importlib.util.find_spec', return_value=object()), \
                    patch('subprocess.check_call') as pip:
                exec(compile(source, '<dependency-cell>', 'exec'), {})
                pip.assert_not_called()
        self.assertGreater(checked, 0)

    def test_only_missing_package_is_requested(self):
        for path, cell, source in cells():
            if 'package-install' not in cell['metadata'].get('tags', []):
                continue
            tree = ast.parse(source)
            required = next(ast.literal_eval(node.generators[0].iter)
                            for node in ast.walk(tree) if isinstance(node, ast.ListComp))
            missing = required[-1]
            with self.subTest(path=path, cell=cell['id']), \
                    patch('importlib.util.find_spec', side_effect=lambda name: None if name == missing else object()), \
                    patch('subprocess.check_call') as pip:
                exec(compile(source, '<dependency-cell>', 'exec'), {})
                pip.assert_called_once_with([sys.executable, '-m', 'pip', 'install', '-q', missing])


if __name__ == '__main__':
    unittest.main()
