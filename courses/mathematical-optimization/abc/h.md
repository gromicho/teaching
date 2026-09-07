# H — Holistic convex optimization

Subgradient methods, Newton steps and Lagrange duality. Suggested classes: 11, 12.

## Learning progression

1. Implement and inspect progress and projection strategies.
2. Distinguish primal variables, multipliers, relaxed subproblem solutions and subgradients.
3. Connect multiplier domains and update signs to the chosen primal/dual convention.

## Discuss and investigate

- Does a small change in successive iterates prove optimality?
- When must multipliers be projected onto a nonnegative or nonpositive domain?
- Which code should remain visible in the algorithm lesson and which should later applications import?

## Version choice

The public Holistic notebook retains the full strategy-based progression and all four original examples, including alternative abstract-model duals. Dependencies enter at their teaching stage. The dual update direction is explicit, actual Ipopt subproblems execute, and the finite example's duality gap is shown.

## Notebook

[Open Holistic convex optimization on GitHub](https://github.com/gromicho/teaching/blob/main/foundations/optimization/holistic-convex-optimization.ipynb) · [Run in Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/foundations/optimization/holistic-convex-optimization.ipynb).

[Back to the ABC sequence](README.md).
