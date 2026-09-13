"""Exercise feedback must detect bad plans, not merely execute an empty scaffold."""
import contextlib
import io
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ExerciseFeedbackTests(unittest.TestCase):
    def load_check(self, name):
        path = ROOT / 'courses/abw/notebooks/optimization' / (name + '.ipynb')
        nb = json.loads(path.read_text(encoding='utf-8'))
        namespace = {}
        for cell in nb['cells']:
            if cell['id'] in ['cell-003', 'independent-plan-check']:
                exec(''.join(cell['source']), namespace)
        return namespace['check_plan']

    def test_feasible_plans_and_independent_constraint_failures(self):
        # Feasible examples are deliberately not an answer key of optimal plans.
        examples = [
            ('alva-electric', dict(asset_1=200, asset_2=200, asset_3=200),
             dict(asset_1=200, asset_2=0, asset_3=0), 'Year 20'),
            ('feed-three-ingredients', {'Barley': .8, 'Corn': .12, 'Sunflower Seed': .08},
             {'Barley': .79, 'Corn': .12, 'Sunflower Seed': .09}, 'Sunflower'),
            ('weenies-and-buns', {0: 100, 1: 100}, {0: 4000, 1: 100}, 'Resource 1'),
            ('worldlight-indexed', {'product_1': 10, 'product_2': 10},
             {'product_1': 0, 'product_2': 61}, 'product_2'),
        ]
        for name, good, bad, label in examples:
            with self.subTest(notebook=name), contextlib.redirect_stdout(io.StringIO()):
                check = self.load_check(name)
                self.assertTrue(check(good)['feasible'])
                result = check(bad)
                self.assertFalse(result['feasible'])
                self.assertTrue(any(label in text and not passed for text, passed in result['checks'].items()))
                with self.assertRaisesRegex(ValueError, 'exactly the keys'):
                    check({})
                nonfinite = dict(good)
                nonfinite[next(iter(good))] = float('nan')
                with self.assertRaisesRegex(ValueError, 'finite numerical'):
                    check(nonfinite)
                self.assertEqual(check(good), check(good), 'Rerunning a check must not change the plan.')


if __name__ == '__main__':
    unittest.main()
