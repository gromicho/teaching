# Notebook setup and verification

Updated 30 August 2026. The 2026/27 course materials are still in preparation, not frozen. The setup cleanup applies to the maintained shared-foundations and ABW notebooks, with matching changes to the private ABW keys. Historical notebooks are preserved unchanged.

## What students actually need

A package used by a lesson does not necessarily need installing: it may already be available. An exact version in our [maintenance requirements](../requirements.txt) records a tested baseline, not a demonstrated minimum version.

Google's published [2026.07 CPU-runtime package snapshot](https://raw.githubusercontent.com/googlecolab/backend-info/ec53f93fe44a9cab118dc5451527b18e36e1a643/pip-freeze.txt) includes NetworkX 3.6.1, Matplotlib 3.10.0, Pyomo 6.10.1 and HiGHS's Python package (`highspy`) 1.15.1. This is evidence about that snapshot, not a check of every student's running session. Colab updates its preinstalled software; see its [runtime-version guidance](https://research.google.com/colaboratory/runtime-version-faq.html).

For example, the unnecessary graph-lesson installation cell has been removed:

```python
%pip install -q networkx==3.6.1 "matplotlib==3.11.1"
```

It enforced exact versions and would request a Matplotlib upgrade on the documented runtime. The graph lesson does not need that upgrade. Quotation marks were harmless; the issue was the unnecessary installation/version constraint.

## Findings in the supplied lesson code

| Lesson | Current setup |
| --- | --- |
| Python primer and ABW Python practice | Standard-library code; no package installation is needed. |
| ABW shortest path A to F | Uses Colab's NetworkX; no Matplotlib dependency or installation cell. |
| NetworkX introduction | Uses Colab's NetworkX and Matplotlib without forcing upgrades. |
| ABW linear-optimization exercises and the repeated-solves lesson | Retain only Pyomo/HiGHS setup, reduced from ten explicitly installed packages. |
| Feed Calculator and Timor-Leste shared preparation | No solver initialization. Use Colab's data-reading libraries and, for Feed Calculator, Matplotlib indirectly through pandas. |
| Alice nonlinear optimization | Uses Pyomo for the formulation and SciPy for the numerical calculation, with SymPy, NumPy and Matplotlib. Do not add HiGHS as a nonlinear solver. |
| Optional street-network example | Installs only OSMnx explicitly. Live map services still need separate verification; this is not covered by the offline tests. |

These are findings about the supplied code, not all possible student extensions. Indirect dependencies matter: absence of an explicit import alone is not proof that a package is unused.

## Why keep the short solver setup?

The retained `%pip install -q pyomo==6.10.1 highspy==1.15.1` line ensures the versions used to test solver availability, persistent solves and termination handling. When matching versions are already installed, pip leaves them satisfied; on an older or local runtime it supplies the tested solver packages. Alice only specifies Pyomo because its numerical solve uses SciPy, not HiGHS. These version checks are deliberate compatibility safeguards, not a claim that every Colab session lacks a solver.

For local Jupyter use, install the dependencies in a separate environment. The [maintenance baseline](../requirements-test.txt) covers the routine core notebooks, not the optional map lesson or specialist advanced cases; students using Colab should not install that full list over Colab's existing environment.

## Maintenance policy

1. Keep learner setup specific to the notebook: use compatible preinstalled libraries, and install only missing packages or versions required by a documented compatibility issue. Keep setup visible and understandable.
2. Keep the tested Pyomo/HiGHS baseline and explicit solver-availability/termination checks in optimization lessons. Check the selected runtime before deciding an installation is needed; do not assume these packages are always absent from Colab.
3. Keep maintenance pins in an isolated test environment. Do not replace Colab's complete scientific stack simply to match that environment.
4. Run both test profiles, including installation cells, and check dependency conflicts. A final classroom check should also use a fresh actual Colab browser session.
5. Update development course selections as material improves. The historical `v2026.1` checkpoint can remain for provenance; it does not freeze the forthcoming course. Agree and record the final annual edition before distribution.

## What the checks establish

The [execution checker](../scripts/check_resources.py) runs fresh kernels using temporary copies. With `--execute --run-setup`, it executes the remaining installation cells as well as the lesson; without `--run-setup`, it retains the original preinstalled-dependencies mode.

Automated checks cover the [maintenance baseline](../requirements-test.txt) and a [Colab-library compatibility profile](../requirements-colab-test.txt). The latter matches the relevant scientific-library versions in Google's 2026.07 CPU snapshot, not every package or operating-system detail of Colab. Neither profile alone establishes that the browser experience or live map services work. A final check in a fresh actual Colab session remains appropriate before classroom distribution.
