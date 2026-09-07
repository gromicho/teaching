# Versions, names and selection decisions

The MO 2020–2021 family is the most coherent long ABC sequence among the sources inspected. The shorter *Optimization Stories in Logistics and Transportation* family uses a different naming scheme. Later ABW/AABW notebook names move again. Match equations, datasets and learning purpose before matching names.

| Teaching content | MO 2020–2021 name | Other observed names |
| --- | --- | --- |
| Stable vase and symbolic/numerical optimization | Alice | Alice |
| Linear trophy production | Betty | Caroline |
| Purchasing, batches, discounts and inventory | Caroline | Hilda; later Francis |
| Weak/strong facility location | Dina | Gina; later Elizabeth |
| Assignment algorithm versus LP | ExploringLAP | Older network-optimization notebook |
| Maximum-volume cylinder | Francis | Betty |
| Empirical uncertainty and robust production | Joan and Karin | Els and Fiona |

The earlier A–H family also contains Dick's bin/table-packing case. It is a useful additional example, not a reason to rename or duplicate the longer MO sequence.

## Selected full source versions

### A — Alice (42 cells)

Source: `Lectures/Notebooks for lectures/Alice.ipynb`.

The 42-cell MO lecture retains the physical derivation, symbolic versus numeric pi, plots, Pyomo introspection and deliberate late solver installation. The current 10-cell public companion is tested but shorter; use it for execution, not as evidence that the longer narrative is already restored.

### B — Betty (49 cells)

Source: `Lectures/Notebooks for lectures/Betty.ipynb`.

Use the MO Betty story to fix the ABC naming. The 79-cell maintained Caroline production-planning notebook is the strongest current implementation of this same LP lesson: three actual engines, alternative indexed formulations, slacks, duals and model inspection. It is substantially richer than the short later Caroline introduction.

### C — Caroline (55 cells)

Source: `Lectures/Notebooks for lectures/Caroline.ipynb`.

The 55-cell MO Caroline notebook develops the material-planning model step by step. It is the same case later called Hilda and Francis, not the later Caroline LP. Preserve the construction sequence privately; the maintained Francis instructor key provides the tested full-case solution. A student-facing worked edition still needs preparation.

### D — Dina (15 cells)

Source: `Lectures/Notebooks for lectures/Dina.ipynb`.

Keep the MO Dina case and weak/strong formulation derivation. Use the tested Elizabeth notebook for current execution and its real multi-engine comparison. The original 50-facility/100-customer experiment remains a useful scaling extension, not a replacement for comparing LP bounds.

### E — Exploring LAP (19 cells)

Source: `Lectures/Notebooks for lectures/ExploringLAP.ipynb`.

Use the 19-cell abstract-model version rather than the earlier 11-cell fragment. It actually compares SciPy assignment with CBC and GLPK. Its 10,000-by-10,000 default would create 100 million variables; preserve the scaling question but choose a bounded default when modernizing. E is the ExploringLAP filename, not an invented character.

### F — Francis (9 cells)

Source: `Lectures/Notebooks for lectures/Francis.ipynb`.

Use the MO cylinder notebook and its maximum-volume subject. It is a short bridge, not the material-planning notebook recently supplied under the same name. Its original installer and missing qualified solver imports need repair before a maintained public edition is released.

### G — Global and convex optimization (36 cells)

Source: `Lectures/Notebooks for lectures/Global.ipynb`.

The 36-cell Global notebook is the coherent lecture, while Untitled8/9 provide supplementary examples. Keep initial-point sensitivity, nonlinear test functions and convex modeling. Correct the blanket complexity statements, replace unrestricted eval and avoid automatic remote submissions.

### H — Holistic convex optimization (66 cells)

Source: `Lectures/Notebooks for lectures/Holistic convex optimization .ipynb`.

Choose the full 66-cell lecture, not the 34-cell Week 3 draft. It connects symbolic derivatives to strategies, Newton steps, projection and abstract Pyomo Lagrangian subproblems, including alternative duals of the same problem. It explicitly teaches delayed imports and avoiding copy-and-paste.

### I — Ignacio (50 cells)

Source: `Lectures/Notebooks for lectures/Ignacio blends with uncertain data.ipynb`.

Choose the 50-cell lecture over the 48-cell checkpoint. It links repeated blending solves, simulations, averages and extremes with symbolic value-function analysis and optional animations. Preserve the distinction between optimizing averaged inputs and averaging optimized outcomes.

### JK — Joan and Karin (58 cells)

Source: `Lectures/Notebooks for lectures/Joan and Karin's story on week 5.ipynb`.

Choose the 58-cell lecture, not the 56-cell Copy or 51-cell Week 5 predecessor. J and K share one notebook: Joan analyzes observations; Karin builds box, budget/cardinality and ball uncertainty models, then continuous and mixed-integer conic versions. Keep the actual Ipopt/Gurobi/CPLEX/Xpress roles and later introductions.

## What this selection does and does not establish

All chosen files were read from the recovered source collection. The source hashes are recorded in `sequence.json`; private archive copies have separate destination hashes because saved outputs are cleared and account-specific remote email configuration is removed. Original bytes remain in the local project sandbox.

A/B/D have tested public companions. That does not certify every cell of their longer historical sources. C has a maintained private full-case key, not a public answer notebook. E/F/G/H/I/JK are content-selected sources and study guides here; complete modern public executions remain future preparation work. This readiness distinction prevents a course map from being mistaken for a fully rebuilt runnable course.
