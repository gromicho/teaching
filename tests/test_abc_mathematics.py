"""Independent checks for mathematical repairs in the ABC lecture notebooks."""
import ast
import json
from pathlib import Path
import unittest

import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[1]


def functions_from(path,cell_ids,namespace):
    """Load the actual displayed definitions without executing demonstration cells."""
    nb=json.loads((ROOT/path).read_text(encoding='utf-8'))
    for cell in nb['cells']:
        if cell['id'] in cell_ids:
            tree=ast.parse(''.join(cell['source']))
            definitions=[node for node in tree.body if isinstance(node,ast.FunctionDef)]
            exec(compile(ast.Module(body=definitions,type_ignores=[]),str(path),'exec'),namespace)
    return namespace


class BlendingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.namespace=functions_from('foundations/optimization/ignacio-stochastic-blending.ipynb',{'source-040'}, {})

    def test_piecewise_value_matches_independent_lp_in_both_regions(self):
        value=self.namespace['optimalValue']
        points=[(1,1),(1,1/3),(4,1),(4,1/3),(1.2,.9),(1.5,6/7),(1.75,1)]
        rng=np.random.default_rng(17)
        points.extend(zip(rng.uniform(1,4,30),rng.uniform(1/3,1,30)))
        for a,b in points:
            with self.subTest(a=a,b=b):
                result=linprog([1,1],A_ub=[[-a,-1],[-b,-1]],b_ub=[-7,-4],bounds=[(0,None),(0,None)],method='highs')
                self.assertTrue(result.success)
                self.assertAlmostEqual(value((a,b)),result.fun,places=7)

    def test_negative_intersection_is_not_returned_as_a_feasible_solution(self):
        a,b=1.2,.9
        self.assertLess((4*a-7*b)/(a-b),0)
        self.assertAlmostEqual(self.namespace['optimalValue']((a,b)),7/a)

    def test_outside_the_stated_support_is_rejected(self):
        with self.assertRaises(ValueError):self.namespace['optimalValue']((0.5,0.5))


class DualDirectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.namespace=functions_from('foundations/optimization/holistic-convex-optimization.ipynb',{'source-009','source-029','source-031','source-036'}, {})

    def test_explicit_minimization_and_maximization_converge(self):
        driver=self.namespace['SubgradientForLagrangeDuals']
        for sense,sign in [('min',1),('max',-1)]:
            relaxation=lambda u:(sign*(u-2)**2,sign*2*(u-2))
            with self.subTest(sense=sense):
                result=driver(0.0,relaxation,50,sense=sense)
                self.assertAlmostEqual(result,2.0,places=9)

    def test_projection_respects_multiplier_domain(self):
        driver=self.namespace['SubgradientForLagrangeDuals']
        result=driver(1.0,lambda u:(-(u+1)**2,-2*(u+1)),50,project=lambda u:max(0,u),sense='max')
        self.assertEqual(result,0.0)

    def test_finite_example_dual_bound_has_the_documented_gap(self):
        relaxation=self.namespace['relaxationExampleTwo']
        candidates=[(0,0),(0,4),(4,4),(4,0),(1,2),(2,1)]
        primal=min(-2*x+y for x,y in candidates if x+y==3)
        self.assertEqual(primal,-3)
        self.assertEqual(relaxation(2.0)[0],-6)
        for u in np.linspace(-5,5,31):
            value,gradient=relaxation(u)
            self.assertLessEqual(value,primal)
            for other in [u-.1,u+.1]:
                # A supergradient of a concave dual supports it from above.
                self.assertLessEqual(relaxation(other)[0],value+gradient*(other-u)+1e-9)


if __name__=='__main__':unittest.main()
