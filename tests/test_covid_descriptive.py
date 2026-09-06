"""Exercise the COVID notebook's actual aggregation cells without network access."""
import json
from pathlib import Path
import unittest
import warnings

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / 'courses/aabw/notebooks/lecture-2/descriptive-analytics-covid.ipynb'


class CovidDescriptiveTests(unittest.TestCase):
    def setUp(self):
        # Match the JHU layout: four metadata columns followed by daily counts.
        # Two nonadjacent provinces belong to the same country.
        self.covid = pd.DataFrame({
            'Province/State': ['North', None, 'South'],
            'Country/Region': ['Zeta', 'Alpha', 'Zeta'],
            'Lat': [10.0, 20.0, 30.0],
            'Long': [40.0, 50.0, 60.0],
            '1/22/20': [1, 7, 3],
            '1/23/20': [2, 8, 5],
            '1/24/20': [4, 9, 6],
        })
        notebook = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
        cells = {cell['id']: cell for cell in notebook['cells']}
        scope = {'covid': self.covid}
        # Test source cells, not a second implementation of their calculation.
        with warnings.catch_warnings():
            warnings.simplefilter('error', FutureWarning)
            for cell_id in ('c015-fa1bfb5430', 'c018-223515aae6'):
                source = ''.join(cells[cell_id]['source'])
                exec(compile(source, f'{NOTEBOOK.name}:{cell_id}', 'exec'), scope)
        self.grouped = scope['grouped']

    def test_provinces_are_summed_by_country_for_each_date(self):
        expected = pd.DataFrame(
            [[7, 8, 9], [4, 7, 10]],
            index=pd.Index(['Alpha', 'Zeta'], name='Country/Region'),
            columns=['1/22/20', '1/23/20', '1/24/20'],
        )
        pd.testing.assert_frame_equal(self.grouped, expected)

    def test_grouping_preserves_daily_totals_and_plot_orientation(self):
        dates = ['1/22/20', '1/23/20', '1/24/20']
        pd.testing.assert_series_equal(
            self.grouped.sum(), self.covid[dates].sum(),
        )
        self.assertEqual(self.grouped.T.index.tolist(), dates)
        self.assertEqual(self.grouped.T.columns.tolist(), ['Alpha', 'Zeta'])


if __name__ == '__main__':
    unittest.main()
