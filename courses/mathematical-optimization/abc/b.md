# B — Betty

Nonlinear modeling: the cylinder of maximum volume. Suggested classes: 2.

## Learning progression

1. Formulate radius and height decisions with a surface-area budget.
2. Separate a nonlinear mathematical expression from a solver interface.
3. Compare a numerical candidate with analytical reasoning, and account for degenerate starting points.

## Discuss and investigate

- Why can a starting point at zero be problematic?
- Does a local nonlinear solver certify global optimality here?
- Can eliminating one variable make the geometry easier to understand?

## Version choice

The public Betty notebook uses the original cylinder story, symbolic reduction and a checked local Ipopt model. It introduces solver discovery and installation after the geometric derivation. The archived MO variant calls the cylinder Francis; that alias does not change the teaching name.

## Notebook

[Open Betty on GitHub](https://github.com/gromicho/teaching/blob/main/foundations/optimization/betty-cylinder.ipynb) · [Run in Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/foundations/optimization/betty-cylinder.ipynb).

[Back to the ABC sequence](README.md).
