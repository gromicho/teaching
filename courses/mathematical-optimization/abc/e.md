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

Use the 19-cell abstract-model version rather than the earlier 11-cell fragment. It actually compares SciPy assignment with CBC and GLPK. Its 10,000-by-10,000 default would create 100 million variables; preserve the scaling question but choose a bounded default when modernizing. E is the ExploringLAP filename, not an invented character.

## Current material

Selected historical source in the private companion; a maintained public notebook is still pending.

[Back to the ABC sequence](README.md).
