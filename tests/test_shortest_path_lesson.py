"""Cross-check the taught implementations on the same weighted problem."""
import json
from pathlib import Path
import sys
from time import perf_counter
import unittest

import highspy
import networkx as nx
import numpy as np
import pandas as pd
import pyomo.environ as pyo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'support'))
from teaching_utils import solve_checked


def lesson_functions():
    relative = 'courses/aabw/notebooks/lecture-2/shortest-path-optimization-vs-algorithms.ipynb'
    nb = json.loads((ROOT / relative).read_text(encoding='utf-8'))
    ns = {'nx': nx, 'np': np, 'pd': pd, 'pyo': pyo, 'solve_checked': solve_checked,
          'solver_name': 'appsi_highs', 'pc': perf_counter, 'environment': {}}
    prefixes = ['validate-path-input', 'c014-', 'c016-', 'c019-', 'c021-', 'c023-', 'c025-', 'c033-']
    for cell in nb['cells']:
        if any(cell['id'].startswith(prefix) for prefix in prefixes):
            exec(''.join(cell['source']), ns)
    return ns


class ShortestPathLessonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ns = lesson_functions()
        highspy.Highs.resetGlobalScheduler(True)

    @classmethod
    def tearDownClass(cls):
        highspy.Highs.resetGlobalScheduler(True)

    def test_weighted_route_differs_from_minimum_hops(self):
        g = nx.DiGraph()
        g.add_weighted_edges_from([('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 9)], weight='length')
        self.assertEqual(nx.shortest_path_length(g, 'A', 'C'), 1)
        for name in ['SolveAsLO', 'SimpleDijkstra', 'Dijkstra', 'nx_sp']:
            with self.subTest(strategy=name):
                path, distance = self.ns[name](g, 'A', 'C')
                self.assertAlmostEqual(distance, 2)
                if name != 'SolveAsLO':
                    self.assertEqual(path, ['A', 'B', 'C'])

    def test_both_graph_and_weights_are_reproducible(self):
        make = self.ns['GenerateGraph']
        a, b, c = make(40, seed=11), make(40, seed=11), make(40, seed=12)
        self.assertEqual(set(a.edges()), set(b.edges()))
        self.assertEqual(nx.get_edge_attributes(a, 'length'), nx.get_edge_attributes(b, 'length'))
        self.assertNotEqual(nx.get_edge_attributes(a, 'length'), nx.get_edge_attributes(c, 'length'))

    def test_random_graph_agreement_including_linear_model(self):
        for seed in [5, 17, 81]:
            g = self.ns['GenerateGraph'](15, seed)
            reference = nx.shortest_path_length(g, 0, 14, weight='length')
            for name in ['SolveAsLO', 'SimpleDijkstra', 'Dijkstra', 'nx_sp']:
                with self.subTest(seed=seed, strategy=name):
                    _, distance = self.ns[name](g, 0, 14)
                    self.assertAlmostEqual(distance, reference)

    def test_heap_handles_float_weights_and_incomparable_labels(self):
        g = nx.DiGraph()
        g.add_edge('start', 1, length=0.1)
        g.add_edge('start', ('other',), length=0.1)
        g.add_edge(1, 'end', length=0.2)
        g.add_edge(('other',), 'end', length=0.2)
        path, distance = self.ns['Dijkstra'](g, 'start', 'end')
        self.assertEqual(path[0], 'start')
        self.assertEqual(path[-1], 'end')
        self.assertAlmostEqual(distance, 0.3)

    def test_unreachable_and_invalid_weights_are_reported(self):
        g = nx.Graph()
        g.add_nodes_from(['A', 'B'])
        for name in ['SimpleDijkstra', 'Dijkstra', 'nx_sp']:
            with self.subTest(strategy=name):
                with self.assertRaises(nx.NetworkXNoPath):
                    self.ns[name](g, 'A', 'B')
        for invalid in [-1, np.inf, np.nan, None]:
            g = nx.Graph()
            g.add_edge('A', 'B', **({} if invalid is None else {'length': invalid}))
            for name in ['ShortestPathAsLinearOptimization', 'SimpleDijkstra', 'Dijkstra', 'nx_sp']:
                with self.subTest(weight=invalid, strategy=name):
                    with self.assertRaisesRegex(ValueError, 'nonnegative'):
                        self.ns[name](g, 'A', 'B')

    def test_bad_comparison_stops_before_reporting_timings(self):
        def unweighted(g, s, t):
            return nx.shortest_path(g, s, t), nx.shortest_path_length(g, s, t)
        with self.assertRaisesRegex(AssertionError, 'weighted distance'):
            self.ns['DoThese'](12, [unweighted], repeats=2)

    def test_repeated_measurements_do_not_accumulate_between_calls(self):
        strategies = [self.ns['Dijkstra'], self.ns['nx_sp']]
        first, values = self.ns['DoThese'](12, strategies, repeats=2)
        second, again = self.ns['DoThese'](12, strategies, repeats=2)
        self.assertEqual(len(first.attrs['samples']), 4)
        self.assertEqual(len(second.attrs['samples']), 4)
        self.assertEqual(values.iloc[0].nunique(), 1)
        pd.testing.assert_frame_equal(values, again)


if __name__ == '__main__':
    unittest.main()
