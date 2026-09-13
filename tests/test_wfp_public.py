"""Check the worked nominal scaffold without publishing the robust answer."""
from collections import namedtuple
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


def notebook(name):
    return json.loads((ROOT / 'courses/aabw/notebooks/wfp-syria' / name).read_text(encoding='utf-8'))


class WfpPublicTests(unittest.TestCase):
    def test_nominal_model_uses_hard_availability_and_conserves_each_food(self):
        highspy.Highs.resetGlobalScheduler(True)
        try:
            cells = notebook('robust-optimization-companion.ipynb')['cells']
            source = next(''.join(c['source']) for c in cells
                          if ''.join(c['source']).startswith('def WFP_model'))
            ns = {'pd': pd, 'pyo': pyo}
            exec(source, ns)
            Data = namedtuple('Data', 'NodesTypes EdgesCost FoodNutritionalValue FoodCost FoodInternationalPrice NutrientRequirements')
            names = ['Supplier S', 'Transfer TS', 'Demand D', 'Isolated TS']
            nodes = pd.DataFrame({'Name': names, 'Type': ['R', 'TS', 'D', 'TS'],
                                  'Demand': [0, 0, 2, 0]}, index=names)
            arcs = pd.DataFrame({'tCost': [1, 1]}, index=pd.MultiIndex.from_tuples(
                [(names[0], names[1]), (names[1], names[2])]))
            nutrients = pd.DataFrame({'Energy': [10, 10]}, index=['Available', 'Unavailable'])
            local = pd.DataFrame({'NodeName': [names[0]], 'FoodName': ['Available'], 'Mean': [3]})
            international = pd.DataFrame(columns=['FoodName', 'InternationalPrice'])
            requirements = pd.DataFrame({'Type': ['adult'], 'Energy': [5], 'Iodine(ug)': [1]})
            model = ns['WFP_model'](Data(nodes, arcs, nutrients, local, international, requirements))
            solve_checked(model)
            self.assertAlmostEqual(pyo.value(model.R['Available']), 0.5)
            self.assertAlmostEqual(pyo.value(model.R['Unavailable']), 0)
            self.assertAlmostEqual(pyo.value(model.Cost), 5)
            self.assertEqual(model.F[names[0], names[1], 'Unavailable'].ub, 0)
            self.assertEqual(pyo.value(model.total_holding_costs), 0)
            self.assertNotIn('Iodine(ug)', model.L)
            self.assertIn(names[3], model.NT)
            self.assertLess(max(pyo.value(v) for v in model.pc.values()), 100)
        finally:
            highspy.Highs.resetGlobalScheduler(True)

    def test_robust_part_remains_a_nutrient_uncertainty_exercise(self):
        for filename in ['starter-data-visualization.ipynb', 'robust-optimization-companion.ipynb']:
            with self.subTest(notebook=filename):
                cells = notebook(filename)['cells']
                source = next(''.join(c['source']) for c in cells
                              if ''.join(c['source']).startswith('def robust_WFP_model'))
                self.assertIn('NotImplementedError', source)
                markdown = '\n'.join(''.join(c['source']) for c in cells if c['cell_type'] == 'markdown')
                self.assertIn('uncertainty in nutritional values', markdown)
                self.assertNotIn('<!--', markdown)
                self.assertIn('sigma_l', markdown)


if __name__ == '__main__':
    unittest.main()
