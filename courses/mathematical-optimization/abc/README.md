# The ABC of Mathematical Optimization

**Recommended backbone: A–K, in ten core notebooks.** Joan and Karin share the last notebook. This is the longest coherent alphabetical teaching family found in the collected MO 2020–2021, ABW and AABW material. E means *Exploring LAP*, G means *Global*, and H means *Holistic*; they are notebook titles, not invented character names.

The progression is modeling → linear optimization → mixed-integer models → formulation strength → specialized algorithms → nonlinear/convex optimization → duality → stochastic optimization → robust/conic optimization. Keep this progression, and use richer later implementations where they improve the same lesson.

This folder is the **public course guide and version selection**. It links to canonical tested notebooks rather than duplicating them. The complete selected sources and exercise/capstone answers are in the separate private companion. Several advanced sources still need modernization before they have a maintained public notebook; the table states that explicitly.

| Stage | Lesson | Main subject | Current public notebook |
| --- | --- | --- | --- |
| A | [Alice](a.md) | From a story to an objective; symbolic and numerical optimization | [Alice: symbolic and numerical optimization](https://github.com/gromicho/teaching/blob/main/foundations/optimization/alice-optimization.ipynb) |
| B | [Betty](b.md) | Linear programming, indexed models, slacks and duals | [Caroline: production planning](https://github.com/gromicho/teaching/blob/main/foundations/optimization/caroline-production-planning.ipynb) |
| C | [Caroline](c.md) | Mixed-integer purchasing and inventory planning | Selected source; public notebook pending |
| D | [Dina](d.md) | Facility location and formulation strength | [Elizabeth: weak and strong formulations](https://github.com/gromicho/teaching/blob/main/foundations/optimization/elizabeth-location-models.ipynb) |
| E | [Exploring LAP](e.md) | Assignment algorithms versus an LP model | Selected source; public notebook pending |
| F | [Francis](f.md) | Nonlinear modeling: the cylinder of maximum volume | Selected source; public notebook pending |
| G | [Global and convex optimization](g.md) | Local optima, convexity and equivalent representations | Selected source; public notebook pending |
| H | [Holistic convex optimization](h.md) | Subgradient methods, Newton steps and Lagrange duality | Selected source; public notebook pending |
| I | [Ignacio](i.md) | Stochastic programming and uncertain nutrient coefficients | Selected source; public notebook pending |
| JK | [Joan and Karin](jk.md) | From empirical uncertainty to robust and conic optimization | Selected source; public notebook pending |

## How long should the course be?

I recommend **18 core classes**, followed by **three wind-energy capstone classes** and **five exercise sessions**. This is a suggested 26-session teaching plan, not a count of 26 distinct notebooks or an estimate of classroom hours. The source backbone has 399 cells across ten notebooks; cell count records completeness, not teaching quality. See [the schedule](SCHEDULE.md).

The wind capstones turn the same application into three distinct modeling questions: discrete site selection and big-M; continuous placement with wake and depth effects; conic reformulation and robust wind uncertainty. Keep their answer notebooks private. The tested instructor version of the first wind assignment already exists; the later two remain selected historical sources.

## Which versions are best?

- **A:** the full 42-cell MO Alice for the narrative, with the tested public Alice as the numerical companion. Do not confuse the shorter runnable notebook with a full restoration of the source explanation.
- **B:** MO Betty establishes the naming; the maintained 79-cell Caroline LP notebook supplies the best current worked implementation, including three real solver engines, slacks and duals.
- **C:** MO Caroline is material planning, corresponding to later Hilda/Francis. Keep the tested full-case Francis key private.
- **D:** MO Dina plus the tested Elizabeth formulation/solver comparison.
- **E–I:** the full MO lecture versions, especially Holistic (66 cells) and Ignacio (50), rather than short drafts/checkpoints.
- **J–K:** the 58-cell Joan/Karin version, which extends the 56-cell copy and 51-cell predecessor.

See [the version and alias comparison](VERSIONS.md) and the machine-readable [sequence](sequence.json).

## Useful branches without padding the alphabet

Insert WorldLight and Weenies & Buns after B to practice indexed formulations. Add Dick's bin/table packing after C if discrete modeling needs more practice. Add shortest paths and TSP after E to explore network algorithms and subtour formulations. Use Feed Calculator, Timor-Leste or WFP as application branches after the relevant modeling/uncertainty stages. These are extensions, not additional alphabet letters and not interchangeable copies of the same case.

Ready public practice: [WorldLight](https://github.com/gromicho/teaching/blob/main/courses/abw/notebooks/optimization/worldlight-indexed.ipynb), [Weenies & Buns](https://github.com/gromicho/teaching/blob/main/courses/abw/notebooks/optimization/weenies-and-buns.ipynb), [shortest path: model versus algorithm](https://github.com/gromicho/teaching/blob/main/foundations/networks/shortest-path-optimization-vs-algorithms.ipynb), [Feed Calculator preparation](https://github.com/gromicho/teaching/blob/main/foundations/cases/feed-calculator-preparation.ipynb), and [Timor-Leste preparation](https://github.com/gromicho/teaching/blob/main/foundations/cases/timor-leste-preparation.ipynb). Check each notebook's catalogue profile before including it in an assessed release.

## Preserve the teaching method

When a lesson teaches installation, solver discovery, model inspection or an algorithm, show the relevant implementation. Ordinary applications import stable helpers from `support/teaching_utils.py`. Preserve deliberately late installation/imports, especially Alice and Holistic. A solver comparison must execute distinct engines on equivalent fresh models, and an algorithm/model comparison must actually run both. Time-limited incumbents are not certificates of optimality. Do not replace rich teaching code with a short script solely to make a validation check green.

This selection is for course development; it is not a frozen cohort release. No historical installer, remote submission or instructor answer was published as a new runnable student lesson by creating this guide.
