# Story names and selected versions

The teaching name identifies the mathematical case. This curated sequence preserves Betty's nonlinear cylinder and Caroline's linear trophy production. It combines useful versions across teaching families rather than reproducing the MO 2020–2021 alphabet unchanged.

| Case | Name in this guide | Historical aliases |
| --- | --- | --- |
| Stable vase | Alice | Alice |
| Maximum-volume cylinder | Betty | Francis in MO 2020–2021 |
| Linear trophy production | Caroline | Betty in MO 2020–2021 |
| Purchasing and inventory | Francis | Hilda in Optimization Stories; Caroline in MO 2020–2021 |
| Facility location | Dina | Gina; later Elizabeth |
| Assignment algorithm versus LP | Exploring LAP | ExploringLAP |
| Empirical and robust uncertainty | Joan and Karin | Related earlier Els/Fiona stories |

The original `Colab Notebooks/Betty.ipynb` explicitly states the cylinder problem: maximize pi*r^2*h with 2*pi*r^2 + 2*pi*r*h <= 12 and nonnegative radius and height. This is nonlinear. Caroline instead maximizes trophy profit under linear resource constraints. They are not duplicate lessons.

Historical archive filenames and notebook titles remain intact as provenance. The manifest records both the guide name and the historical source name, with its original hash. In particular, the archived file `f-francis.ipynb` is the cylinder source selected for B; `b-betty.ipynb` is the LP source selected for C; and `c-caroline.ipynb` is the inventory source selected for F.

## Public editions and historical sources

### A — Alice

[Public notebook](https://github.com/gromicho/teaching/blob/main/foundations/optimization/alice-optimization.ipynb).

The 42-cell MO lecture retains the physical derivation, symbolic versus numeric pi, plots, Pyomo introspection and deliberate late solver installation. The current 10-cell public companion is tested but shorter; use it for execution, not as evidence that the longer narrative is already restored.

Historical source: `Lectures/Notebooks for lectures/Alice.ipynb` (42 cells).

### B — Betty

[Public notebook](https://github.com/gromicho/teaching/blob/main/foundations/optimization/betty-cylinder.ipynb).

The public Betty notebook uses the original cylinder story, symbolic reduction and a checked local Ipopt model. It introduces solver discovery and installation after the geometric derivation. The archived MO variant calls the cylinder Francis; that alias does not change the teaching name.

Historical source: `Lectures/Notebooks for lectures/Francis.ipynb` (9 cells).

### C — Caroline

[Public notebook](https://github.com/gromicho/teaching/blob/main/foundations/optimization/caroline-production-planning.ipynb).

Caroline is the linear trophy-production story. Use the maintained 79-cell Caroline notebook for its indexed formulations, actual Ipopt/CBC/HiGHS comparison, slacks and duals. The selected 49-cell MO source calls this same LP Betty; retain that source title in provenance, not as the teaching name here. This case is distinct from Betty's nonlinear cylinder.

Historical source: `Lectures/Notebooks for lectures/Betty.ipynb` (49 cells).

### D — Dina

[Public notebook](https://github.com/gromicho/teaching/blob/main/foundations/optimization/elizabeth-location-models.ipynb).

Keep the MO Dina case and weak/strong formulation derivation. Use the tested Elizabeth notebook for current execution and its real multi-engine comparison. The original 50-facility/100-customer experiment remains a useful scaling extension, not a replacement for comparing LP bounds.

Historical source: `Lectures/Notebooks for lectures/Dina.ipynb` (15 cells).

### E — Exploring LAP

[Public notebook](https://github.com/gromicho/teaching/blob/main/foundations/optimization/exploring-assignment.ipynb).

The public assignment notebook retains the abstract Pyomo model and runs SciPy, CBC and GLPK on the same matrix. GLPK uses its portable Python bindings. A bounded default replaces the original 100-million-variable model; scaling remains an explicit experiment.

Historical source: `Lectures/Notebooks for lectures/ExploringLAP.ipynb` (19 cells).

### F — Francis

[Public notebook](https://github.com/gromicho/teaching/blob/main/courses/abw/notebooks/optimization/francis-material-planning.ipynb).

The public Francis notebook contains the full purchasing/inventory case, original data, material-requirement calculation and staged modeling tasks. It is a student exercise notebook. The completed purchasing model and its solution remain private. Historical aliases include Hilda and MO Caroline.

Historical source: `Lectures/Notebooks for lectures/Caroline.ipynb` (55 cells).

### G — Global and convex optimization

[Public notebook](https://github.com/gromicho/teaching/blob/main/foundations/optimization/global-and-convex-optimization.ipynb).

The public Global notebook retains local-start experiments, expected DCP rejections, both convex reformulations and real Ipopt/CPLEX/Gurobi/Xpress solves. It corrects the cylinder radius bound and the reversed inequality in the quadratic reformulation; mathematical functions replace unrestricted eval.

Historical source: `Lectures/Notebooks for lectures/Global.ipynb` (36 cells).

### H — Holistic convex optimization

[Public notebook](https://github.com/gromicho/teaching/blob/main/foundations/optimization/holistic-convex-optimization.ipynb).

The public Holistic notebook retains the full strategy-based progression and all four original examples, including alternative abstract-model duals. Dependencies enter at their teaching stage. The dual update direction is explicit, actual Ipopt subproblems execute, and the finite example's duality gap is shown.

Historical source: `Lectures/Notebooks for lectures/Holistic convex optimization .ipynb` (66 cells).

### I — Ignacio

[Public notebook](https://github.com/gromicho/teaching/blob/main/foundations/optimization/ignacio-stochastic-blending.ipynb).

The public Ignacio notebook retains the original LP, simulation, symbolic candidate analysis, integration and animation. A corrected piecewise value function handles a zero second-ingredient quantity and is checked against actual CBC solutions. It distinguishes scenario-wise optima from a fixed decision chosen before observation.

Historical source: `Lectures/Notebooks for lectures/Ignacio blends with uncertain data.ipynb` (50 cells).

### JK — Joan and Karin

[Public notebook](https://github.com/gromicho/teaching/blob/main/foundations/optimization/joan-karin-robust-optimization.ipynb).

The public Joan/Karin notebook retains the observed data, box/Gamma counterparts and both conic representations. It corrects aliased lower/upper dictionaries, keeps the cone-side sign condition, and runs Ipopt plus all three commercial conic engines. Independent enumeration checks the integer conic optimum.

Historical source: `Lectures/Notebooks for lectures/Joan and Karin's story on week 5.ipynb` (58 cells).

The historical selection remains ten notebooks containing 399 cells. Modern editions differ because of corrected mathematics, current APIs, added verification and student/instructor separation. See [modernization provenance](../../../provenance/2026-09-07-abc-public-notebooks.json).
