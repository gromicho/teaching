# E — Exploring LAP

Assignment algorithms versus an LP model. Suggested classes: 6.

## Learning progression

1. Build the bipartite assignment model from a cost matrix.
2. Explain the integral extreme points of the assignment polytope.
3. Compare a dedicated assignment algorithm with actual LP solves, including memory and model-building costs.

## Discuss and investigate

- Why can this assignment model use continuous nonnegative variables?
- What changes if additional side constraints are introduced?
- What grows quadratically with the number of items?

## Version choice

The public assignment notebook retains the abstract Pyomo model and runs SciPy, CBC and GLPK on the same matrix. GLPK uses its portable Python bindings. A bounded default replaces the original 100-million-variable model; scaling remains an explicit experiment.

## Notebook

[Open Exploring LAP on GitHub](https://github.com/gromicho/teaching/blob/main/foundations/optimization/exploring-assignment.ipynb) · [Run in Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/foundations/optimization/exploring-assignment.ipynb).

[Back to the ABC sequence](README.md).
