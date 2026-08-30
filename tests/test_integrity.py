import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('integrity',ROOT/'scripts/check_integrity.py')
CHECK=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        (self.root/'provenance').mkdir()
        (self.root/'catalog.json').write_text(json.dumps({'repository':'gromicho/teaching','visibility':'public','notebooks':[]}))
        (self.root/'example.md').write_text('Public fixture')
        self.record={'path':'example.md','source_visibility':'public','destination_sha256':CHECK.sha(self.root/'example.md')}
        self.save()

    def save(self):
        (self.root/'provenance/imports.json').write_text(json.dumps({'imports':[self.record]}))

    def tearDown(self):
        self.tmp.cleanup()

    def test_public_source_allowed(self):
        self.assertEqual(CHECK.check(self.root),[])

    def test_private_source_rejected(self):
        self.record['source_visibility']='private'
        self.save()
        self.assertTrue(any('Private source' in x for x in CHECK.check(self.root)))

    def test_private_filename_rejected(self):
        (self.root/'demo-solution.ipynb').write_text('{}')
        self.assertTrue(any('private-boundary' in x for x in CHECK.check(self.root)))

    def test_history_does_not_freeze_development(self):
        (self.root/'example.md').write_text('Reviewed correction')
        self.assertEqual(CHECK.check(self.root),[])
        self.assertTrue(CHECK.check(self.root,verify_import_snapshot=True))

    def test_absent_course_selection_rejected(self):
        folder=self.root/'courses/abw/editions'
        folder.mkdir(parents=True)
        (folder/'2026-2027.json').write_text(json.dumps({'foundations':['missing.ipynb'],'course_resources':[],'datasets':[]}))
        self.assertTrue(any('Course selection' in x for x in CHECK.check(self.root)))


if __name__=='__main__':
    unittest.main()
