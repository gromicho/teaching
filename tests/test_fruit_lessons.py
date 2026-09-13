"""Check the data and mathematics students actually execute in the fruit pair."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
from scipy.stats import entropy
from sklearn import tree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'support'))
from fruit_utils import fix_fruit_outliers

LECTURE3 = 'courses/abw/notebooks/lecture-3/fruit-data-exploration.ipynb'
LECTURE4 = 'courses/abw/notebooks/lecture-4/accuracy-entropy-and-clustering.ipynb'


def sources(relative):
    notebook = json.loads((ROOT / relative).read_text(encoding='utf-8'))
    return {cell['id']: ''.join(cell['source']) for cell in notebook['cells']}


def raw_data():
    return pd.read_csv(ROOT / 'data/fruits.csv', sep=';', decimal=',')


class FruitCorrectionTests(unittest.TestCase):
    def test_exact_corrections_preserve_every_other_value(self):
        raw = raw_data()
        saved = raw.copy(deep=True)
        expected = raw.copy(deep=True)
        expected.loc[19, ['Length', 'Width']] = [7.2, 2.5]
        expected.loc[20, ['Length', 'Width']] = [2.53, 2.77]
        actual = fix_fruit_outliers(raw)
        pd.testing.assert_frame_equal(actual, expected)
        pd.testing.assert_frame_equal(raw, saved)
        self.assertEqual(len(actual), 92)
        pd.testing.assert_frame_equal(fix_fruit_outliers(actual), actual)

    def test_reordered_labels_and_unrelated_extrema(self):
        raw = raw_data().sample(frac=1, random_state=8)
        raw.index = ['fruit-' + str(i) for i in raw.index]
        raw['note'] = 'retain this column'
        raw.loc['unusual', :] = ['Pear', 0.01, 99.0, 'retain this too']
        result = fix_fruit_outliers(raw)
        self.assertEqual(result.loc['fruit-19', 'Width'], 2.5)
        self.assertAlmostEqual(result.loc['fruit-20', 'Length'], 2.53)
        pd.testing.assert_series_equal(result.loc['unusual'], raw.loc['unusual'])
        self.assertEqual(result.index.tolist(), raw.index.tolist())
        pd.testing.assert_series_equal(result['note'], raw['note'])
        pd.testing.assert_frame_equal(fix_fruit_outliers(result), result)

    def test_lecture3_explanation_matches_helper_and_survives_reruns(self):
        cells = sources(LECTURE3)
        raw = raw_data()
        saved = raw.copy(deep=True)
        ns = {'raw_fruits': raw}
        for _ in range(2):
            for cell_id in ['original-007', 'original-008', 'original-009']:
                exec(cells[cell_id], ns)
            pd.testing.assert_frame_equal(ns['fruits'], fix_fruit_outliers(raw))
            for cell_id in ['original-009', 'original-008', 'original-008', 'original-009']:
                exec(cells[cell_id], ns)
                pd.testing.assert_frame_equal(ns['fruits'], fix_fruit_outliers(raw))
        pd.testing.assert_frame_equal(raw, saved)

    def test_lecture4_loader_survives_reruns(self):
        source = sources(LECTURE4)['original-006']
        ns = {'pd': pd, 'data_path': ROOT / 'data/fruits.csv',
              'fix_fruit_outliers': fix_fruit_outliers}
        exec(source, ns)
        first = ns['fruits'].copy(deep=True)
        exec(source, ns)
        pd.testing.assert_frame_equal(ns['fruits'], first)
        pd.testing.assert_frame_equal(first, fix_fruit_outliers(raw_data()))

    def test_standalone_helper_replaces_old_cache_and_rejects_bad_download(self):
        source = sources(LECTURE4)['fruit-helper']
        payload = (ROOT / 'support/fruit_utils.py').read_bytes()
        self.assertIn(hashlib.sha256(payload).hexdigest(), source)
        for bad_payload in [False, True]:
            with self.subTest(bad_payload=bad_payload), tempfile.TemporaryDirectory() as tmp:
                support = Path(tmp)
                helper = support / 'fruit_utils.py'
                helper.write_text('# older cached edition\n', encoding='utf-8')
                with patch('urllib.request.urlopen') as fetch:
                    fetch.return_value.read.return_value = b'wrong bytes' if bad_payload else payload
                    ns = {'support_path': support, 'hashlib': hashlib,
                          'urlopen': fetch}
                    if bad_payload:
                        with self.assertRaisesRegex(ValueError, 'checksum'):
                            exec(source, ns)
                        self.assertEqual(helper.read_text(), '# older cached edition\n')
                    else:
                        exec(source, ns)
                        self.assertEqual(helper.read_bytes(), payload)
                        exec(source, ns)
                        fetch.assert_called_once()


class FruitEntropyTests(unittest.TestCase):
    def test_both_lessons_use_actual_tree_membership(self):
        for relative in [LECTURE3, LECTURE4]:
            with self.subTest(notebook=relative):
                cells = sources(relative)
                ns = {'fruits': fix_fruit_outliers(raw_data()), 'pd': pd,
                      'np': np, 'tree': tree, 'display': lambda *args: None}
                exec(cells['entropy-tree'], ns)
                function_id = 'original-018' if relative == LECTURE3 else 'original-019'
                exec(cells[function_id], ns)
                for cell_id in ['entropy-node-counts', 'entropy-split', 'entropy-gain']:
                    exec(cells[cell_id], ns)
                self.assertEqual(ns['node_counts'].tolist(), [0, 20, 25, 2])
                self.assertEqual(ns['split_counts'].sum(axis=1).tolist(), [27, 20])
                np.testing.assert_array_equal(ns['split_counts'].sum(axis=0), ns['node_counts'])
                expected = 27 / 47 * entropy([25 / 27, 2 / 27], base=2)
                self.assertAlmostEqual(ns['weighted_entropy'], expected)
                parent = ns['parent_id']
                model = ns['entropy_tree'].tree_
                self.assertAlmostEqual(ns['parent_entropy'], model.impurity[parent])
                self.assertGreater(ns['information_gain'], 0)
                # Executing the calculation again must not accumulate counts.
                exec(cells['entropy-split'], ns)
                self.assertAlmostEqual(ns['weighted_entropy'], expected)


if __name__ == '__main__':
    unittest.main()
