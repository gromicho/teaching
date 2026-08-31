"""The public Sudoku starter prepares clues; it must not contain a solved grid."""
import contextlib
import io
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / 'courses/aabw/notebooks/sudoku/starter.ipynb'


class SudokuStarterTests(unittest.TestCase):
    def test_preparation_runs_without_a_solver(self):
        notebook = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
        scope = {}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code':
                    self.assertEqual(cell['outputs'], [])
                    self.assertIsNone(cell['execution_count'])
                    exec(compile(''.join(cell['source']), '<sudoku-starter>', 'exec'), scope)
        puzzle = scope['start_sudoku']
        self.assertEqual(puzzle.shape, (9, 9))
        self.assertEqual(puzzle.loc[1].tolist(), [7, 0, 0, 0, 2, 0, 4, 8, 0])
        self.assertEqual(puzzle.loc[9].tolist(), [0, 9, 3, 0, 4, 0, 0, 0, 7])
        self.assertTrue(puzzle.isin(range(10)).all().all())
        self.assertGreater(int((puzzle == 0).sum().sum()), 0)
        self.assertIn('_', output.getvalue())
        self.assertNotIn('pyomo', scope)
        self.assertNotIn('gurobipy', scope)


if __name__ == '__main__':
    unittest.main()
