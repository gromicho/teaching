# The ABC of Mathematical Optimization

**Open a notebook below, or run it directly in Colab.** Every stage has a public notebook. Francis is a student case and modeling exercise; its completed solution and the weekly exercise keys remain private.

Start with Alice, Betty and Caroline: stable vase, nonlinear cylinder and linear trophy production. Continue through algorithms and duality to stochastic, robust and conic optimization. Shared notebooks are maintained once in the collection and linked here.

| Stage | Notebook | Subject | Run |
| --- | --- | --- | --- |
| A | [Alice](https://github.com/gromicho/teaching/blob/main/foundations/optimization/alice-optimization.ipynb) | From a story to an objective; symbolic and numerical optimization | [Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/foundations/optimization/alice-optimization.ipynb) |
| B | [Betty](https://github.com/gromicho/teaching/blob/main/foundations/optimization/betty-cylinder.ipynb) | Nonlinear modeling: the cylinder of maximum volume | [Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/foundations/optimization/betty-cylinder.ipynb) |
| C | [Caroline](https://github.com/gromicho/teaching/blob/main/foundations/optimization/caroline-production-planning.ipynb) | Linear programming, indexed models, slacks and duals | [Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/foundations/optimization/caroline-production-planning.ipynb) |
| D | [Dina](https://github.com/gromicho/teaching/blob/main/foundations/optimization/elizabeth-location-models.ipynb) | Facility location and formulation strength | [Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/foundations/optimization/elizabeth-location-models.ipynb) |
| E | [Exploring LAP](https://github.com/gromicho/teaching/blob/main/foundations/optimization/exploring-assignment.ipynb) | Assignment algorithms versus an LP model | [Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/foundations/optimization/exploring-assignment.ipynb) |
| F | [Francis](https://github.com/gromicho/teaching/blob/main/courses/abw/notebooks/optimization/francis-material-planning.ipynb) | Mixed-integer purchasing and inventory planning — student exercise | [Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/courses/abw/notebooks/optimization/francis-material-planning.ipynb) |
| G | [Global and convex optimization](https://github.com/gromicho/teaching/blob/main/foundations/optimization/global-and-convex-optimization.ipynb) | Local optima, convexity and equivalent representations | [Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/foundations/optimization/global-and-convex-optimization.ipynb) |
| H | [Holistic convex optimization](https://github.com/gromicho/teaching/blob/main/foundations/optimization/holistic-convex-optimization.ipynb) | Subgradient methods, Newton steps and Lagrange duality | [Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/foundations/optimization/holistic-convex-optimization.ipynb) |
| I | [Ignacio](https://github.com/gromicho/teaching/blob/main/foundations/optimization/ignacio-stochastic-blending.ipynb) | Stochastic programming and uncertain nutrient coefficients | [Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/foundations/optimization/ignacio-stochastic-blending.ipynb) |
| JK | [Joan and Karin](https://github.com/gromicho/teaching/blob/main/foundations/optimization/joan-karin-robust-optimization.ipynb) | From empirical uncertainty to robust and conic optimization | [Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/foundations/optimization/joan-karin-robust-optimization.ipynb) |

## Teaching sequence

Use [the suggested schedule](SCHEDULE.md): 18 core classes, three wind-energy capstones and five practice sessions. These are suggested teaching blocks, not 26 distinct notebooks. Joan and Karin share the final notebook.

Study guides: [A](a.md) · [B](b.md) · [C](c.md) · [D](d.md) · [E](e.md) · [F](f.md) · [G](g.md) · [H](h.md) · [I](i.md) · [JK](jk.md).

The names come from several course versions. **Betty is the cylinder; Caroline is the LP; Francis is purchasing/inventory.** Historical filenames remain documented in [the version map](VERSIONS.md). The public notebooks are modernized teaching editions; the full historical sources retain their original names privately.

## What the notebooks preserve

- Betty derives the geometry before introducing the numerical solver.
- Assignment actually runs SciPy, CBC and GLPK on common data.
- Global compares local starting points, demonstrates DCP rejection and reformulation, and runs four solver engines.
- Holistic retains the reporting/projection strategies, all four examples and actual Lagrangian subproblem solves, with dependencies introduced when needed.
- Ignacio progresses from repeated LP solves to symbolic active-set reasoning, integration and accelerated simulation. Its corrected value function respects nonnegative ingredient quantities.
- Joan/Karin develops observed uncertainty, box and budgeted counterparts, and both continuous and mixed-integer cone formulations. All named conic engines execute; independent enumeration checks the integer result.

Ordinary package and solver utilities are imported from `support/teaching_utils.py`; algorithm implementations remain visible where they are being taught. Instructor answers are not needed to run the public lecture examples.

## Extend the course

After Caroline, use [WorldLight](https://github.com/gromicho/teaching/blob/main/courses/abw/notebooks/optimization/worldlight-indexed.ipynb) and [Weenies & Buns](https://github.com/gromicho/teaching/blob/main/courses/abw/notebooks/optimization/weenies-and-buns.ipynb) for indexed formulations. After assignment, use [shortest paths: optimization versus algorithms](https://github.com/gromicho/teaching/blob/main/foundations/networks/shortest-path-optimization-vs-algorithms.ipynb). The wind capstones and additional weekly exercise keys are organized in the private companion.
