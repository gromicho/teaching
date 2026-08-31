"""Preserve Jeff's contribution without opening the public instructor boundary."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import check_integrity
import check_resources
from publication_policy import public_notebook_error

RELATIVE = 'archive/jeff-kantor-solver-installation-legacy.ipynb'


class HistoricalReferenceTests(unittest.TestCase):
    def setUp(self):
        self.item = {'id':'historical-test', 'path':RELATIVE, 'kind':'historical-reference',
                     'execution_profile':'archive', 'collection':'historical'}

    def test_approved_reference_is_not_a_general_exception(self):
        self.assertIsNone(public_notebook_error(self.item))
        self.assertIsNotNone(public_notebook_error(dict(self.item,path='archive/another.ipynb')))
        self.assertIsNotNone(public_notebook_error(dict(self.item,path='another.ipynb')))
        self.assertIsNotNone(public_notebook_error(dict(self.item,kind='solution')))
        self.assertIsNotNone(public_notebook_error(dict(self.item,execution_profile='core')))
        self.assertIsNotNone(public_notebook_error(dict(self.item,kind='worked-example',execution_profile='core')))

    def test_attribution_and_retained_content_hash(self):
        record=json.loads((ROOT/'provenance/jeff-kantor-restoration-2026-08-31.json').read_text(encoding='utf-8'))
        payload=(ROOT/RELATIVE).read_bytes()
        self.assertEqual(hashlib.sha256(payload).hexdigest(),record['destination_sha256'])
        notebook=json.loads(payload)
        retained=[{'cell_type':c['cell_type'],'source':''.join(c['source'])} for c in notebook['cells'][1:]]
        fingerprint=json.dumps(retained,ensure_ascii=False,separators=(',', ':')).encode('utf-8')
        self.assertEqual(hashlib.sha256(fingerprint).hexdigest(),record['retained_cells_sha256'])
        self.assertIn('Jeff Kantor',retained[0]['source'])
        self.assertIn('great friend',retained[0]['source'])
        self.assertIn('do not use Run all',''.join(notebook['cells'][0]['source']))
        self.assertEqual(notebook['metadata']['teaching']['execution_profile'],'archive')
        for cell in notebook['cells']:
            if cell['cell_type']=='code':
                self.assertFalse(cell['outputs'])
                self.assertIsNone(cell['execution_count'])

    def make_fixture(self, folder):
        root=Path(folder)
        (root/'archive').mkdir()
        (root/'provenance').mkdir()
        shutil.copyfile(ROOT/RELATIVE,root/RELATIVE)
        (root/'catalog.json').write_text(json.dumps({'repository':'gromicho/teaching','visibility':'public','notebooks':[self.item]}),encoding='utf-8')
        (root/'provenance/imports.json').write_text(json.dumps({'imports':[{'path':RELATIVE,'source_visibility':'public','destination_sha256':check_integrity.sha(root/RELATIVE)}]}),encoding='utf-8')
        return root

    def test_historical_notebook_is_never_executed(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.make_fixture(folder)
            with patch.object(check_resources,'NotebookClient',side_effect=AssertionError('Historical code must not run')):
                report=check_resources.check(root,execute=True,run_setup=True)
            self.assertEqual(report['errors'],[])
            self.assertEqual(report['results'][0]['structure'],'pass')
            self.assertEqual(report['results'][0]['execution'],'excluded: archive')

    def test_unapproved_archive_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.make_fixture(folder)
            self.assertEqual(check_integrity.check(root),[])
            (root/'archive/another.ipynb').write_text('{}',encoding='utf-8')
            self.assertTrue(any('private-boundary' in error for error in check_integrity.check(root)))

    def test_archive_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.make_fixture(folder)
            with (root/RELATIVE).open('ab') as stream:
                stream.write(b'\n')
            self.assertTrue(any('checksum mismatch' in error for error in check_integrity.check(root)))

    def test_current_editions_do_not_select_the_archive(self):
        for path in (ROOT/'courses').glob('*/editions/*.json'):
            edition=json.loads(path.read_text(encoding='utf-8'))
            self.assertNotIn(RELATIVE,edition['foundations']+edition['course_resources'])

    def test_historical_course_selection_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root=self.make_fixture(folder)
            editions=root/'courses/test/editions'
            editions.mkdir(parents=True)
            (editions/'test.json').write_text(json.dumps({'foundations':[RELATIVE], 'course_resources':[], 'datasets':[]}),encoding='utf-8')
            self.assertTrue(any('not a current course selection' in error for error in check_integrity.check(root)))


if __name__=='__main__':
    unittest.main()
