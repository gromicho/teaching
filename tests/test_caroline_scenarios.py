import json
from pathlib import Path
import sys
import unittest

import highspy
import pandas as pd
import pyomo.environ as pyo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'support'))
from teaching_utils import solve_checked


class CarolineScenarioTests(unittest.TestCase):
    def test_scenarios_preserve_the_original_stock_and_do_not_accumulate(self):
        highspy.Highs.resetGlobalScheduler(True)
        try:
            nb = json.loads((ROOT / 'foundations/optimization/caroline-production-planning.ipynb').read_text())
            cells = {c['id']: ''.join(c['source']) for c in nb['cells']}
            ns = {'pd': pd, 'pyo': pyo, 'solve_checked': solve_checked, 'SOLVER': 'appsi_highs',
                  'solutions': pd.DataFrame()}
            for key in ['cell-025', 'cell-029', 'cell-033']:
                exec(cells[key], ns)
            original = ns['baseline_materials'].copy(deep=True)
            for _ in range(2):
                for key in ['cell-036', 'cell-037', 'cell-038']:
                    exec(cells[key], ns)
                self.assertAlmostEqual(ns['solutions'].loc['value', 'added 1 plaque'], 17706)
                self.assertAlmostEqual(ns['solutions'].loc['value', 'added 1 plaque and 5 dm wood'], 17713.5)
                pd.testing.assert_frame_equal(ns['materials'], original)
                pd.testing.assert_frame_equal(ns['baseline_materials'], original)
            self.assertEqual(len(ns['solutions'].columns), 2)
            baseline = ns['CreateThirdVersionOfCaroline'](ns['trophies'], original)
            solve_checked(baseline)
            self.assertAlmostEqual(pyo.value(baseline.profit), 17700)
        finally:
            highspy.Highs.resetGlobalScheduler(True)


if __name__ == '__main__':
    unittest.main()
