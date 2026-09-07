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

Choose the full 66-cell lecture, not the 34-cell Week 3 draft. It connects symbolic derivatives to strategies, Newton steps, projection and abstract Pyomo Lagrangian subproblems, including alternative duals of the same problem. It explicitly teaches delayed imports and avoiding copy-and-paste.

## Current material

Selected historical source in the private companion; a maintained public notebook is still pending.

[Back to the ABC sequence](README.md).
