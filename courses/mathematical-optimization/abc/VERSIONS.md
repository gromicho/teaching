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

## Selected sources

### A — Alice

Historical source: `Lectures/Notebooks for lectures/Alice.ipynb` (42 cells).

The 42-cell MO lecture retains the physical derivation, symbolic versus numeric pi, plots, Pyomo introspection and deliberate late solver installation. The current 10-cell public companion is tested but shorter; use it for execution, not as evidence that the longer narrative is already restored.

### B — Betty

Historical source: `Lectures/Notebooks for lectures/Francis.ipynb` (9 cells).

Betty is the nonlinear maximum-volume cylinder story in the original Optimization Stories family (Colab Notebooks/Betty.ipynb, eight cells). The selected nine-cell MO source calls this same cylinder Francis; that is a historical alias, not this guide's lesson name. It has the same volume objective and surface-area budget. Its installer and unqualified solver calls still need modernization. Betty must not link to Caroline's linear trophy-production notebook.

### C — Caroline

Historical source: `Lectures/Notebooks for lectures/Betty.ipynb` (49 cells).

Caroline is the linear trophy-production story. Use the maintained 79-cell Caroline notebook for its indexed formulations, actual Ipopt/CBC/HiGHS comparison, slacks and duals. The selected 49-cell MO source calls this same LP Betty; retain that source title in provenance, not as the teaching name here. This case is distinct from Betty's nonlinear cylinder.

### D — Dina

Historical source: `Lectures/Notebooks for lectures/Dina.ipynb` (15 cells).

Keep the MO Dina case and weak/strong formulation derivation. Use the tested Elizabeth notebook for current execution and its real multi-engine comparison. The original 50-facility/100-customer experiment remains a useful scaling extension, not a replacement for comparing LP bounds.

### E — Exploring LAP

Historical source: `Lectures/Notebooks for lectures/ExploringLAP.ipynb` (19 cells).

Use the 19-cell abstract-model version rather than the earlier 11-cell fragment. It actually compares SciPy assignment with CBC and GLPK. Its 10,000-by-10,000 default would create 100 million variables; preserve the scaling question but choose a bounded default when modernizing. E is the ExploringLAP filename, not an invented character.

### F — Francis

Historical source: `Lectures/Notebooks for lectures/Caroline.ipynb` (55 cells).

Francis is the purchasing and inventory case in the current ABW materials, also called Hilda in Optimization Stories and Caroline in MO 2020–2021. The selected 55-cell MO source preserves its stepwise development; the maintained private Francis notebook provides the full-case key. The MO notebook titled Francis instead describes Betty's cylinder, so identify the case by its equations and data.

### G — Global and convex optimization

Historical source: `Lectures/Notebooks for lectures/Global.ipynb` (36 cells).

The 36-cell Global notebook is the coherent lecture, while Untitled8/9 provide supplementary examples. Keep initial-point sensitivity, nonlinear test functions and convex modeling. Correct the blanket complexity statements, replace unrestricted eval and avoid automatic remote submissions.

### H — Holistic convex optimization

Historical source: `Lectures/Notebooks for lectures/Holistic convex optimization .ipynb` (66 cells).

Choose the full 66-cell lecture, not the 34-cell Week 3 draft. It connects symbolic derivatives to strategies, Newton steps, projection and abstract Pyomo Lagrangian subproblems, including alternative duals of the same problem. It explicitly teaches delayed imports and avoiding copy-and-paste.

### I — Ignacio

Historical source: `Lectures/Notebooks for lectures/Ignacio blends with uncertain data.ipynb` (50 cells).

Choose the 50-cell lecture over the 48-cell checkpoint. It links repeated blending solves, simulations, averages and extremes with symbolic value-function analysis and optional animations. Preserve the distinction between optimizing averaged inputs and averaging optimized outcomes.

### JK — Joan and Karin

Historical source: `Lectures/Notebooks for lectures/Joan and Karin's story on week 5.ipynb` (58 cells).

Choose the 58-cell lecture, not the 56-cell Copy or 51-cell Week 5 predecessor. J and K share one notebook: Joan analyzes observations; Karin builds box, budget/cardinality and ball uncertainty models, then continuous and mixed-integer conic versions. Keep the actual Ipopt/Gurobi/CPLEX/Xpress roles and later introductions.

A/C/D have tested public companions. F has a maintained private full-case key. Other selected historical sources still require preparation before public execution; the guide does not certify their old installation cells.
