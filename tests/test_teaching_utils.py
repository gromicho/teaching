"""Protect staged teaching steps and genuinely distinct solver comparisons."""
import ast
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'support'))
import teaching_utils as u

def notebook(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))

def source(cell):return ''.join(cell['source'])

class UtilityTests(unittest.TestCase):
    def test_import_has_no_installation_side_effect(self):
        spec=importlib.util.spec_from_file_location('isolated_utils',ROOT/'support/teaching_utils.py')
        with patch('subprocess.check_call') as call:
            spec.loader.exec_module(importlib.util.module_from_spec(spec))
        call.assert_not_called()

    def test_missing_distribution_uses_import_mapping(self):
        with patch('importlib.util.find_spec',side_effect=lambda name: None if name=='sklearn' else object()), patch('subprocess.check_call') as call:
            self.assertEqual(u.ensure_packages({'numpy':'numpy','sklearn':'scikit-learn'}),['scikit-learn'])
        call.assert_called_once_with([sys.executable,'-m','pip','install','-q','scikit-learn'])

    def test_reset_preserves_fixed_values_inside_nested_blocks(self):
        import pyomo.environ as pyo
        model=pyo.ConcreteModel();model.b=pyo.Block();model.b.x=pyo.Var(initialize=3)
        model.fixed=pyo.Var(initialize=2);model.fixed.fix()
        u.reset_model(model)
        self.assertIsNone(model.b.x.value)
        self.assertEqual(model.fixed.value,2)
        self.assertTrue(model.fixed.fixed)

    def test_failed_solver_is_not_reported_as_a_solution(self):
        with patch.object(u,'make_solver') as factory:
            factory.return_value.available.return_value=False
            with self.assertRaisesRegex(RuntimeError,'unavailable'):
                u.solve_checked(object(),'missing')
            factory.return_value.solve.assert_not_called()

    def test_abw_optimization_packages_are_introduced_later(self):
        cells=notebook('courses/abw/notebooks/python/part-2.ipynb')['cells']
        early=next(c for c in cells if c['id']=='p2-new-data-dependencies')
        later=next(c for c in cells if c['id']=='p2-staged-optimization-packages')
        self.assertNotIn("'pyomo'",source(early));self.assertNotIn("'highspy'",source(early))
        self.assertIn("'pyomo'",source(later));self.assertIn("'highspy'",source(later))
        self.assertGreater(cells.index(later),next(i for i,c in enumerate(cells) if c['id']=='p2-original-037'))

    def test_caroline_comparison_names_three_engines(self):
        for path in ['foundations/optimization/caroline-production-planning.ipynb','courses/aabw/notebooks/lecture-2/caroline-trophy-production.ipynb']:
            comparison=[source(c) for c in notebook(path)['cells'] if 'comparison_rows.append' in source(c)]
            self.assertEqual(len(comparison),3)
            for name in ['ipopt','cbc','appsi_highs']:
                self.assertEqual(sum(f"solve_checked(first, '{name}')" in s for s in comparison),1)
            for s in comparison:
                self.assertIn('CreateFirstVersionOfCaroline()',s)

    def test_elizabeth_commercial_install_stays_after_open_source_comparison(self):
        cells=notebook('courses/aabw/notebooks/lecture-2/elizabeth-facility-location.ipynb')['cells']
        install=next(i for i,c in enumerate(cells) if c['id']=='elizabeth-staged-commercial')
        self.assertTrue(any("solver='cbc'" in source(c) for c in cells[:install]))
        self.assertFalse(any("'gurobipy':" in source(c) for c in cells[:install]))
        run=next(source(c) for c in cells if c['id']=='elizabeth-commercial-comparison')
        for name in ['gurobi_direct','cplex_direct','xpress_direct']:
            self.assertIn(name,run)
        self.assertIn('FacilityLocationWeak',run);self.assertIn('FacilityLocationStrong',run)

    def test_explanatory_functions_match_the_shared_implementation(self):
        tree=ast.parse((ROOT/'support/teaching_utils.py').read_text(encoding='utf-8'))
        expected={n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,ast.FunctionDef)}
        found=set()
        for c in notebook('courses/aabw/notebooks/lecture-2/jeff-kantor-solver-installation.ipynb')['cells']:
            if c['cell_type']!='code':continue
            for n in ast.parse(source(c)).body:
                if isinstance(n,ast.FunctionDef) and n.name in expected:
                    self.assertEqual(ast.dump(n,include_attributes=False),expected[n.name]);found.add(n.name)
        self.assertEqual(found,{'installed_packages','ensure_packages','available_pyomo_solvers','reset_model'})

if __name__=='__main__':unittest.main()
