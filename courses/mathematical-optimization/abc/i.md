# I — Ignacio

Stochastic programming and uncertain nutrient coefficients. Suggested classes: 13, 14.

## Learning progression

1. Model uncertain calcium/protein coefficients and evaluate the resulting decisions.
2. Separate a fixed decision chosen before uncertainty from an adaptive decision chosen after observing it.
3. Compare numerical repeated solves with the derived value function on common observations.

## Discuss and investigate

- Are decisions made before or after the nutrient coefficients are observed?
- Why need the optimum at average data differ from the average of optima?
- How should seed, sample size and evaluation scenarios be controlled in a comparison?

## Version choice

The public Ignacio notebook retains the original LP, simulation, symbolic candidate analysis, integration and animation. A corrected piecewise value function handles a zero second-ingredient quantity and is checked against actual CBC solutions. It distinguishes scenario-wise optima from a fixed decision chosen before observation.

## Notebook

[Open Ignacio on GitHub](https://github.com/gromicho/teaching/blob/main/foundations/optimization/ignacio-stochastic-blending.ipynb) · [Run in Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/foundations/optimization/ignacio-stochastic-blending.ipynb).

[Back to the ABC sequence](README.md).
