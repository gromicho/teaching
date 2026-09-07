# The ABC of Mathematical Optimization

**Start with Alice, Betty and Caroline: stable vase, nonlinear cylinder, linear trophy production.** Betty and Caroline are distinct lessons. Continue through the A–K sequence below to stochastic, robust and conic optimization.

This is a curated sequence across teaching families. It preserves the original Betty/Caroline story names and uses Francis for the current purchasing/inventory case. MO 2020–2021 reused these names: its Betty is the LP, its Caroline is inventory, and its Francis is the cylinder. See [the historical name mapping](VERSIONS.md); do not infer a case from its source filename alone.

The public folder contains course and study guides with links to canonical tested companions. The selected full historical sources and instructor keys are private. A maintained public edition is still pending where indicated.

| Stage | Lesson | Main subject | Current public notebook |
| --- | --- | --- | --- |
| A | [Alice](a.md) | From a story to an objective; symbolic and numerical optimization | [Alice: symbolic and numerical optimization](https://github.com/gromicho/teaching/blob/main/foundations/optimization/alice-optimization.ipynb) |
| B | [Betty](b.md) | Nonlinear modeling: the cylinder of maximum volume | Selected source; public notebook pending |
| C | [Caroline](c.md) | Linear programming, indexed models, slacks and duals | [Caroline: production planning](https://github.com/gromicho/teaching/blob/main/foundations/optimization/caroline-production-planning.ipynb) |
| D | [Dina](d.md) | Facility location and formulation strength | [Elizabeth: weak and strong formulations](https://github.com/gromicho/teaching/blob/main/foundations/optimization/elizabeth-location-models.ipynb) |
| E | [Exploring LAP](e.md) | Assignment algorithms versus an LP model | Selected source; public notebook pending |
| F | [Francis](f.md) | Mixed-integer purchasing and inventory planning | Selected source; public notebook pending |
| G | [Global and convex optimization](g.md) | Local optima, convexity and equivalent representations | Selected source; public notebook pending |
| H | [Holistic convex optimization](h.md) | Subgradient methods, Newton steps and Lagrange duality | Selected source; public notebook pending |
| I | [Ignacio](i.md) | Stochastic programming and uncertain nutrient coefficients | Selected source; public notebook pending |
| JK | [Joan and Karin](jk.md) | From empirical uncertainty to robust and conic optimization | Selected source; public notebook pending |

## Suggested course length

Ten selected source notebooks cover A–K because Joan and Karin share a notebook. Plan 18 core classes, three wind-energy capstone classes and five practice sessions: a suggested 26-session course. The selected sources contain 399 cells; that records completeness, not teaching quality. See [the corrected schedule](SCHEDULE.md).

Betty provides an early concrete nonlinear example after Alice. Caroline then introduces linear structure and dual information. Dina and assignment develop integer formulations and algorithms; Francis combines purchasing, batches and inventory. Global and Holistic revisit nonlinear structure in depth before uncertainty enters through Ignacio, Joan and Karin.

## Version choices and readiness

- A: retain the full Alice narrative and use its tested public companion.
- B: Betty's cylinder, also found under the historical title Francis; modern public edition pending.
- C: use the maintained Caroline LP with actual solver comparisons; the selected historical MO source is titled Betty.
- D: use the maintained Elizabeth companion for Dina's location/formulation lesson.
- F: keep the full purchasing/inventory key private under Francis; its selected MO source is titled Caroline.
- E/G/H/I/JK: retain the full selected lecture sources and their documented modernization work.

The tested public companions are therefore A/C/D. The private maintained inventory key belongs to F. See [version details](VERSIONS.md) and [the sequence manifest](sequence.json).

## Useful branches without padding the alphabet

Insert WorldLight and Weenies & Buns after C to practice indexed formulations. Add Dick's bin/table packing after F if discrete modeling needs more practice. Add shortest paths and TSP after E to explore network algorithms and subtour formulations. Use Feed Calculator, Timor-Leste or WFP as application branches after the relevant modeling/uncertainty stages. These are extensions, not additional alphabet letters and not interchangeable copies of the same case.

Ready public practice: [WorldLight](https://github.com/gromicho/teaching/blob/main/courses/abw/notebooks/optimization/worldlight-indexed.ipynb), [Weenies & Buns](https://github.com/gromicho/teaching/blob/main/courses/abw/notebooks/optimization/weenies-and-buns.ipynb), [shortest path: model versus algorithm](https://github.com/gromicho/teaching/blob/main/foundations/networks/shortest-path-optimization-vs-algorithms.ipynb), [Feed Calculator preparation](https://github.com/gromicho/teaching/blob/main/foundations/cases/feed-calculator-preparation.ipynb), and [Timor-Leste preparation](https://github.com/gromicho/teaching/blob/main/foundations/cases/timor-leste-preparation.ipynb). Check each notebook's catalogue profile before including it in an assessed release.

## Preserve the teaching method

When a lesson teaches installation, solver discovery, model inspection or an algorithm, show the relevant implementation. Ordinary applications import stable helpers from `support/teaching_utils.py`. Preserve deliberately late installation/imports, especially Alice and Holistic. A solver comparison must execute distinct engines on equivalent fresh models, and an algorithm/model comparison must actually run both. Time-limited incumbents are not certificates of optimality. Do not replace rich teaching code with a short script solely to make a validation check green.

This selection is for course development; it is not a frozen cohort release. No historical installer, remote submission or instructor answer was published as a new runnable student lesson by creating this guide.
