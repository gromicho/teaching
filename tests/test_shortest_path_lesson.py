"""Cross-check the taught implementations on the same weighted problem."""
import json
from pathlib import Path
import sys
from time import perf_counter
import unittest
from unittest.mock import patch

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

    def test_unreachable_paths_are_reported_by_the_algorithms(self):
        g = nx.Graph()
        g.add_nodes_from(['A', 'B'])
        self.ns['validate_path_input'](g, 'A', 'B')
        for name in ['SimpleDijkstra', 'Dijkstra', 'nx_sp']:
            with self.subTest(strategy=name):
                with self.assertRaises(nx.NetworkXNoPath):
                    self.ns[name](g, 'A', 'B')

    def test_invalid_weights_are_reported_by_separate_validation(self):
        for invalid in [-1, np.inf, np.nan, None]:
            g = nx.Graph()
            g.add_edge('A', 'B', **({} if invalid is None else {'length': invalid}))
            with self.subTest(weight=invalid):
                with self.assertRaisesRegex(ValueError, 'nonnegative'):
                    self.ns['validate_path_input'](g, 'A', 'B')

    def test_algorithms_do_not_repeat_input_validation(self):
        g = nx.DiGraph()
        g.add_weighted_edges_from([('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 9)], weight='length')
        self.ns['validate_path_input'](g, 'A', 'C')
        def unexpected_validation(*args, **kwargs):
            self.fail('Input validation must not run inside an algorithm.')
        with patch.dict(self.ns, validate_path_input=unexpected_validation):
            for name in ['SolveAsLO', 'SimpleDijkstra', 'Dijkstra', 'nx_sp']:
                with self.subTest(strategy=name):
                    _, distance = self.ns[name](g, 'A', 'C')
                    self.assertAlmostEqual(distance, 2)

    def test_benchmark_validates_each_graph_once_before_any_search_or_clock(self):
        events = []
        validate = self.ns['validate_path_input']
        reference = nx.shortest_path_length
        def checked(g, s, t, attribute='length'):
            events.append(('validate', len(g)))
            validate(g, s, t, attribute)
        def find_reference(g, s, t, **kwargs):
            events.append(('reference', len(g)))
            return reference(g, s, t, **kwargs)
        def strategy(g, s, t):
            events.append(('strategy', len(g)))
            return self.ns['Dijkstra'](g, s, t)
        def clock():
            events.append(('clock', None))
            return perf_counter()
        with patch.dict(self.ns, validate_path_input=checked, pc=clock):
            with patch.object(nx, 'shortest_path_length', find_reference):
                self.ns['DoThese'](21, [strategy], repeats=2)
        expected = []
        for n in [10, 20]:
            expected += [('validate', n), ('reference', n), ('strategy', n)]
            expected += [('clock', None), ('strategy', n), ('clock', None)] * 2
        self.assertEqual(events, expected)

    def test_invalid_benchmark_input_stops_before_reference_or_timing(self):
        g = nx.path_graph(10)
        nx.set_edge_attributes(g, -1, 'length')
        def forbidden(*args, **kwargs):
            self.fail('Invalid input must be rejected before reference, warm-up or timing.')
        with patch.dict(self.ns, GenerateGraph=lambda n: g, pc=forbidden):
            with patch.object(nx, 'shortest_path_length', forbidden):
                with self.assertRaisesRegex(ValueError, 'nonnegative'):
                    self.ns['DoThese'](11, [forbidden])

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
