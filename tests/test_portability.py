import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('portability', ROOT/'scripts/check_portability.py')
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class PortabilityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_unicode_prose_is_preserved(self):
        (self.root/'README.md').write_text('WFP Syria \u2014 example; Do Quynh Anh Ngo; caf\u00e9', encoding='utf-8')
        self.assertEqual(CHECK.check(self.root), [])

    def test_windows_misdecoding_is_caught(self):
        broken = '\u2014'.encode('utf-8').decode('cp1252')
        (self.root/'README.md').write_text(broken, encoding='utf-8')
        self.assertTrue(any('garbled' in error for error in CHECK.check(self.root)))

    def test_non_utf8_file_is_caught(self):
        (self.root/'README.md').write_bytes(b'caf\xe9')
        self.assertTrue(any('UTF-8' in error for error in CHECK.check(self.root)))

    def test_unsafe_path_is_caught(self):
        (self.root/'two words.md').write_text('text', encoding='utf-8')
        self.assertTrue(any('filename' in error for error in CHECK.check(self.root)))

    def test_archive_text_is_not_rewritten_or_rejected(self):
        (self.root/'archive').mkdir()
        path = self.root/'archive/original.md'
        path.write_bytes(b'caf\xe9')
        self.assertEqual(CHECK.check(self.root), [])
        self.assertEqual(path.read_bytes(), b'caf\xe9')


if __name__ == '__main__':
    unittest.main()
