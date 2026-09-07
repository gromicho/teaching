# JK — Joan and Karin

From empirical uncertainty to robust and conic optimization. Suggested classes: 15, 16, 17, 18.

## Learning progression

1. Explain how observations motivate an uncertainty set without treating that set as a probability distribution.
2. Derive and compare box, budgeted and ball-uncertainty counterparts.
3. Keep the nonnegative cone-side condition when squaring a norm inequality; distinguish continuous conic from mixed-integer conic solving.

## Discuss and investigate

- What conservatism is introduced by a box uncertainty set?
- What does the uncertainty budget control?
- Why does dropping the sign restriction when squaring a cone change the feasible set?

## Version choice

The public Joan/Karin notebook retains the observed data, box/Gamma counterparts and both conic representations. It corrects aliased lower/upper dictionaries, keeps the cone-side sign condition, and runs Ipopt plus all three commercial conic engines. Independent enumeration checks the integer conic optimum.

## Notebook

[Open Joan and Karin on GitHub](https://github.com/gromicho/teaching/blob/main/foundations/optimization/joan-karin-robust-optimization.ipynb) · [Run in Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/foundations/optimization/joan-karin-robust-optimization.ipynb).

[Back to the ABC sequence](README.md).
