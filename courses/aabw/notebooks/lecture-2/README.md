# AABW Lecture 2 notebooks

These are the original notebook sources linked from the 2026 *Python for Analytics* Lecture 2 deck. They are kept here separately from the revised `foundations/data-analysis` notebooks because they use different examples and a different teaching sequence.

All notebooks open directly from GitHub in Colab or Binder using the buttons in their opening cell. The two notebooks that use the height--weight example read the maintained repository copy at `data/weight-height.csv`; the original external Gist is no longer available.

The code and author attribution in the recovered notebooks have been retained. Saved execution output was cleared so that students see results produced by their own current runtime.

## Runtime notes

The descriptive, diagnostic, and predictive notebooks use only the shared Python environment. The remaining notebooks demonstrate optimization models. Their legacy cells may request local solvers or commercial packages; these are teaching examples rather than a promise that every solver is available in Binder. In particular, the Jeff Kantor notebook is retained as a solver-installation reference, not as a required student exercise.

## Slide-to-notebook mapping

| Deck topic | Notebook |
| --- | --- |
| Descriptive analytics with COVID data | `descriptive-analytics-covid.ipynb` |
| Diagnostic analytics and statistics | `diagnostic-analytics-statistics.ipynb` |
| Predictive analytics | `predictive-analytics-height-weight.ipynb` |
| Alice: symbolic optimization | `alice-symbolic-optimization.ipynb` |
| Caroline: trophy production | `caroline-trophy-production.ipynb` |
| Shortest paths | `shortest-path-optimization-vs-algorithms.ipynb` |
| Jeff Kantor: solver installation | `jeff-kantor-solver-installation.ipynb` |
| Elizabeth: facility location | `elizabeth-facility-location.ipynb` |
