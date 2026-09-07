# C — Caroline

Linear programming, indexed models, slacks and duals. Suggested classes: 3, 4.

## Learning progression

1. Translate trophy production into a resource-allocation LP and then an indexed model.
2. Separate data, variables, objectives and constraint-generation rules.
3. Explain slacks, binding constraints and dual information, and actually compare solver engines on fresh models.

## Discuss and investigate

- Which resource limits production and which is left over?
- When is it legitimate to interpret a dual value as a marginal value?
- Why can two solvers return slightly different numbers without disagreeing on the optimum?

## Version choice

Caroline is the linear trophy-production story. Use the maintained 79-cell Caroline notebook for its indexed formulations, actual Ipopt/CBC/HiGHS comparison, slacks and duals. The selected 49-cell MO source calls this same LP Betty; retain that source title in provenance, not as the teaching name here. This case is distinct from Betty's nonlinear cylinder.

## Current material

[Caroline: production planning](https://github.com/gromicho/teaching/blob/main/foundations/optimization/caroline-production-planning.ipynb)

[Back to the ABC sequence](README.md).
