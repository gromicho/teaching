# B — Betty

Linear programming, indexed models, slacks and duals. Suggested classes 2, 3.

## Learning progression

1. Translate trophy production into a resource-allocation LP and then an indexed model.
2. Separate data, variables, objectives and constraint-generation rules.
3. Explain slacks, binding constraints and dual information, and actually compare solver engines on fresh models.

## Discuss and investigate

- Which resource limits production and which is left over?
- When is it legitimate to interpret a dual value as a marginal value?
- Why can two solvers return slightly different numbers without disagreeing on the optimum?

## Version choice

Use the MO Betty story to fix the ABC naming. The 79-cell maintained Caroline production-planning notebook is the strongest current implementation of this same LP lesson: three actual engines, alternative indexed formulations, slacks, duals and model inspection. It is substantially richer than the short later Caroline introduction.

## Current material

- [Caroline: production planning](https://github.com/gromicho/teaching/blob/main/foundations/optimization/caroline-production-planning.ipynb) — `core` execution profile.

The current notebook title is retained. The ABC name identifies the teaching role; it does not rename the canonical file.

[Back to the ABC sequence](README.md).
