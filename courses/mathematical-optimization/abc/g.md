# G — Global and convex optimization

Local optima, convexity and equivalent representations. Suggested classes: 9, 10.

## Learning progression

1. Use examples to distinguish local minima from global minima.
2. Check domains and convexity rather than classifying a problem solely by its syntax.
3. Recognize when a reformulation exposes convex structure to a solver.

## Discuss and investigate

- Can an equivalent expression be easier for a modeling system to recognize?
- What assumptions are required before a local optimum is also global?
- Why is a blanket claim about the complexity of all global optimization misleading?

## Version choice

The public Global notebook retains local-start experiments, expected DCP rejections, both convex reformulations and real Ipopt/CPLEX/Gurobi/Xpress solves. It corrects the cylinder radius bound and the reversed inequality in the quadratic reformulation; mathematical functions replace unrestricted eval.

## Notebook

[Open Global and convex optimization on GitHub](https://github.com/gromicho/teaching/blob/main/foundations/optimization/global-and-convex-optimization.ipynb) · [Run in Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/foundations/optimization/global-and-convex-optimization.ipynb).

[Back to the ABC sequence](README.md).
