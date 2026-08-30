"""Exercise migrated WFP resource loaders without running specialist solvers."""
import ast
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

ROOT=Path(__file__).resolve().parents[1]


def loader():
    notebook=json.loads((ROOT/'courses/aabw/notebooks/wfp-syria/starter-data-visualization.ipynb').read_text(encoding='utf-8'))
    source=next(''.join(c['source']) for c in notebook['cells'] if c['cell_type']=='code' and 'RESOURCE_FILES =' in ''.join(c['source']))
    tree=ast.parse('\n'.join(line for line in source.splitlines() if not line.startswith('%')))
    nodes=[node for node in tree.body if
           isinstance(node,ast.FunctionDef) and node.name=='fetch_course_file' or
           isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='RESOURCE_FILES' for t in node.targets)]
    env={'Path':Path,'hashlib':hashlib}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'<resource-loader>','exec'),env)
    return env


class ResourceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.previous=Path.cwd()
        os.chdir(self.tmp.name)
        self.env=loader()

    def tearDown(self):
        os.chdir(self.previous)
        self.tmp.cleanup()

    def test_all_resources_load_from_one_public_source(self):
        def download(url,timeout):
            self.assertEqual(timeout,45)
            prefix='https://raw.githubusercontent.com/gromicho/teaching/main/'
            self.assertTrue(url.startswith(prefix))
            return io.BytesIO((ROOT/url.removeprefix(prefix)).read_bytes())
        self.env['urlopen']=Mock(side_effect=download)
        for name,(relative,expected) in self.env['RESOURCE_FILES'].items():
            path=self.env['fetch_course_file'](name)
            self.assertEqual(path.read_bytes(),(ROOT/relative).read_bytes())
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),expected)

    def test_local_copy_needs_no_network(self):
        name='WFP_Locations.xlsx'
        relative,_=self.env['RESOURCE_FILES'][name]
        path=Path(relative)
        path.parent.mkdir(parents=True)
        path.write_bytes((ROOT/relative).read_bytes())
        self.env['urlopen']=Mock(side_effect=AssertionError('No network expected'))
        self.env['fetch_course_file'](name)
        self.env['urlopen'].assert_not_called()

    def test_mismatched_download_is_not_saved(self):
        self.env['urlopen']=Mock(return_value=io.BytesIO(b'incorrect data'))
        with self.assertRaises(ValueError):
            self.env['fetch_course_file']('WFP_Locations.xlsx')
        self.assertFalse(Path('WFP_Locations.xlsx').exists())

    def test_wrong_existing_file_is_rejected(self):
        Path('WFP_Locations.xlsx').write_bytes(b'wrong local workbook')
        with self.assertRaises(ValueError):
            self.env['fetch_course_file']('WFP_Locations.xlsx')


if __name__=='__main__':
    unittest.main()
