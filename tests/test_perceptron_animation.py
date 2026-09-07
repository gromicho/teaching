"""Check the actual displayed learning and drawing functions on small known cases."""
import ast
import json
from pathlib import Path
import tempfile
import unittest

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import ListedColormap
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = 'foundations/data-analysis/perceptron-learning-animation.ipynb'


class PerceptronTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nb = json.loads((ROOT / NOTEBOOK).read_text(encoding='utf-8'))
        cls.ns = dict(np=np, plt=plt, FuncAnimation=FuncAnimation, ListedColormap=ListedColormap)
        for cell in nb['cells']:
            if cell['id'] in {'predict-rule', 'training-rule', 'boundary-geometry', 'animation-function'}:
                tree = ast.parse(''.join(cell['source']))
                exec(compile(tree, NOTEBOOK, 'exec'), cls.ns)

    def test_hand_computed_negative_example_and_zero_tie(self):
        predict = self.ns['predict']
        self.assertEqual(predict(np.array([2., 1.]), np.zeros(3)), 1)
        result = self.ns['train_perceptron']([[2., 1.]], [-1], max_epochs=1)
        np.testing.assert_allclose(result['weights'], [-.1, -.2, -.1])
        self.assertTrue(result['converged'])
        np.testing.assert_array_equal(result['history'][0]['weights'], [0, 0, 0])
        self.assertFalse(np.shares_memory(result['history'][0]['weights'], result['history'][1]['weights']))

    def test_separable_case_converges_and_xor_does_not(self):
        fit = self.ns['train_perceptron']
        easy = fit([[-1, 0], [1, 0]], [-1, 1], max_epochs=20)
        self.assertTrue(easy['converged'])
        xor = fit([[0, 0], [0, 1], [1, 0], [1, 1]], [-1, 1, 1, -1], max_epochs=5)
        self.assertFalse(xor['converged'])
        self.assertEqual(len(xor['epochs']), 5)
        self.assertGreater(xor['epochs'][-1]['errors_at_epoch_end'], 0)

    def test_shuffle_is_reproducible(self):
        X = [[0, 0], [0, 1], [1, 0], [1, 1]]
        y = [-1, 1, 1, -1]
        a = self.ns['train_perceptron'](X, y, max_epochs=5, shuffle=True, seed=17)
        b = self.ns['train_perceptron'](X, y, max_epochs=5, shuffle=True, seed=17)
        np.testing.assert_array_equal(a['weights'], b['weights'])
        self.assertEqual([h['sample'] for h in a['history']], [h['sample'] for h in b['history']])

    def test_invalid_inputs_are_rejected(self):
        for kwargs in [{'learning_rate': 0}, {'max_epochs': 0}, {'learning_rate': np.nan}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.ns['train_perceptron']([[1, 1]], [-1], **kwargs)
        with self.assertRaises(ValueError):
            self.ns['train_perceptron']([[1, 1]], [0])

    def test_boundary_coordinates_satisfy_the_line_equation(self):
        segment = self.ns['boundary_segment']
        for weights in [np.array([-1., 2., 0.]), np.array([1., 0., 2.]), np.array([1., -3., 2.])]:
            xs, ys = segment(weights, (-2, 2), (-2, 2))
            np.testing.assert_allclose(weights[0] + weights[1]*xs + weights[2]*ys, 0, atol=1e-12)
        xs, ys = segment(np.zeros(3), (-2, 2), (-2, 2))
        self.assertEqual(len(xs), 0)
        self.assertEqual(len(ys), 0)

    def test_animation_shading_errors_and_gif_for_constant_vertical_and_sloping_models(self):
        X = np.array([[-1., -1.], [1., 1.], [0., 1.]])
        y = np.array([-1, 1, -1])
        weights = [np.zeros(3), np.array([0., 1., 0.]), np.array([0., 1., -1.])]
        result = {'history': [dict(weights=w, epoch=i, update=i, sample=None) for i,w in enumerate(weights)]}
        ani, fig, draw, indices = self.ns['make_learning_animation'](X,y,result,['x','y'],{-1:'minus',1:'plus'},max_frames=3)
        try:
            np.testing.assert_array_equal(indices, [0,1,2])
            for i,w in enumerate(weights):
                region, line, rings = draw(i)
                fig.canvas.draw()
                wrong = self.ns['predict'](X,w) != y
                np.testing.assert_array_equal(rings.get_offsets(), X[wrong])
                if i == 0:
                    self.assertTrue(np.all(region.get_array() == 1))
                if i == 1:
                    self.assertTrue(np.all(region.get_array()[:, :60] == -1))
                    self.assertTrue(np.all(region.get_array()[:, 60:] == 1))
            with tempfile.TemporaryDirectory() as temp:
                path = Path(temp)/'perceptron.gif'
                ani.save(path, writer=PillowWriter(fps=2), dpi=40)
                self.assertIn(path.read_bytes()[:6], [b'GIF87a', b'GIF89a'])
        finally:
            plt.close(fig)


if __name__ == '__main__':
    unittest.main()
