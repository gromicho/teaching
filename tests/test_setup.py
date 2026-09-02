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


def cells() -> list[tuple[str, dict[str, object], str]]:
    """Return every cell from every maintained notebook."""
    result: list[tuple[str, dict[str, object], str]] = []
    catalog = json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))
    for item in catalog['notebooks']:
        if item['execution_profile'] == 'archive':
            continue
        notebook = json.loads((ROOT/item['path']).read_text(encoding='utf-8'))
        for cell in notebook['cells']:
            result.append((item['path'], cell, ''.join(cell['source'])))
    return result


def required_packages(source: str) -> dict[str, str]:
    """Extract the import-name to distribution-name mapping from a setup cell."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == 'required_packages'
               for target in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError('Dependency cell has no required_packages mapping')


class SetupTests(unittest.TestCase):
    """Verify notebook dependency safeguards without contacting a package index."""

    def test_every_notebook_has_colab_and_binder_badges(self) -> None:
        """Require both launch choices in every maintained notebook."""
        catalog = json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))
        for item in catalog['notebooks']:
            if item['execution_profile'] == 'archive':
                continue
            notebook = json.loads((ROOT/item['path']).read_text(encoding='utf-8'))
            first_cell = ''.join(notebook['cells'][0]['source'])
            with self.subTest(path=item['path']):
                self.assertIn('colab.research.google.com', first_cell)
                self.assertIn('mybinder.org', first_cell)
                self.assertIn(f'urlpath=tree/{item["path"]}', first_cell)

    def test_no_unconditional_pip_or_version_pins(self) -> None:
        """Reject unconditional pip calls, upgrades, and notebook version pins."""
        for path, cell, source in cells():
            if cell['cell_type'] == 'code':
                with self.subTest(path=path, cell=cell['id']):
                    self.assertFalse(re.search(r'^\s*[%!]pip\s', source, re.MULTILINE))
                    if 'package-install' in cell['metadata'].get('tags', []):
                        self.assertNotIn('==', source)
                        self.assertNotIn('--upgrade', source)

    def test_installed_packages_are_left_alone(self) -> None:
        """Avoid pip entirely when all requested imports are available."""
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

    def test_only_missing_package_is_requested(self) -> None:
        """Install the distribution corresponding to one unavailable import."""
        for path, cell, source in cells():
            if 'package-install' not in cell['metadata'].get('tags', []):
                continue
            required = required_packages(source)
            missing_import, missing_package = list(required.items())[-1]
            with self.subTest(path=path, cell=cell['id']), \
                    patch('importlib.util.find_spec', side_effect=lambda name: None if name == missing_import else object()), \
                    patch('subprocess.check_call') as pip:
                exec(compile(source, '<dependency-cell>', 'exec'), {})
                pip.assert_called_once_with(
                    [sys.executable, '-m', 'pip', 'install', '-q', missing_package]
                )


if __name__ == '__main__':
    unittest.main()
