# Notebook setup and verification

Updated 30 August 2026. The 2026/27 course materials are still in preparation, not frozen. Setup now checks for missing packages in all maintained notebooks, including specialist AABW material and private keys. This is a setup improvement, not a claim that the specialist cases have been fully executed. Historical notebooks are preserved unchanged.

## Colab and Binder

Every maintained notebook provides both an **Open in Colab** badge and an **Open in Binder** badge. Binder constructs the repository environment from the root [`requirements.txt`](../requirements.txt) and [`runtime.txt`](../runtime.txt) before opening a notebook. Colab starts from its own maintained scientific environment.

Each notebook that uses third-party packages also contains a small, tagged dependency safeguard specific to the packages it uses. The safeguard checks import availability first and calls pip only for missing packages. This covers packages that are part of the Binder baseline, packages usually supplied by Colab, and specialist additions such as OSMnx or XlsxWriter. The import name and pip distribution name are recorded separately where they differ, for example `sklearn` and `scikit-learn`.

The Gurobi safeguards can install `gurobipy`, but installation does not provide a licence. The specialist robust-optimization sections still require a valid academic or Web License Service licence.

## What students actually need

A package used by a lesson does not necessarily need installing: it may already be available. An exact version in our [maintenance requirements](../requirements.txt) records a tested baseline, not a demonstrated minimum version.

Google's published [2026.07 CPU-runtime package snapshot](https://raw.githubusercontent.com/googlecolab/backend-info/ec53f93fe44a9cab118dc5451527b18e36e1a643/pip-freeze.txt) includes NetworkX 3.6.1, Matplotlib 3.10.0, Pyomo 6.10.1 and HiGHS's Python package (`highspy`) 1.15.1. This is evidence about that snapshot, not a check of every student's running session. Colab updates its preinstalled software; see its [runtime-version guidance](https://research.google.com/colaboratory/runtime-version-faq.html). Binder uses the repository's declared environment instead of Colab's package snapshot.

For example, the unnecessary graph-lesson installation cell has been removed:

```python
%pip install -q networkx==3.6.1 "matplotlib==3.11.1"
```

It enforced exact versions and would request a Matplotlib upgrade on the documented runtime. The graph lesson does not need that upgrade. Quotation marks were harmless; the issue was the unnecessary installation/version constraint.

## Findings in the supplied lesson code

| Lesson | Current setup |
| --- | --- |
| Python primer and ABW Python practice | Standard-library code; no package installation is needed. |
| ABW shortest path A to F | Checks NetworkX and installs it only if missing; Matplotlib is not required. |
| NetworkX introduction | Checks NetworkX and Matplotlib without forcing upgrades. |
| ABW linear-optimization exercises and the repeated-solves lesson | Check Pyomo and HiGHS, installing either package only if missing. |
| Feed Calculator and Timor-Leste shared preparation | No solver initialization. Check the required data-reading and plotting packages, including the Excel engine. |
| Alice nonlinear optimization | Checks Pyomo, SciPy, SymPy, NumPy and Matplotlib. HiGHS is not a nonlinear solver. |
| Optional street-network example | Installs OSMnx only if missing, without a forced version. Live map services still need separate verification. |
| Specialist AABW notebooks | Check only their requested extras (Pyomo, HiGHS, XlsxWriter or Gurobi); install missing packages without pins. A Gurobi installation does not supply a licence. |

These are findings about the supplied code, not all possible student extensions. Indirect dependencies matter: absence of an explicit import alone is not proof that a package is unused.

## No forced solver versions in learner notebooks

The former exact-version Pyomo/HiGHS installation line was unnecessary when the runtime already supplied these packages. It has been replaced by a short dependency check: when all requested packages are present, **pip is not called at all**. When a package is absent, only that package is requested, without an exact version or upgrade flag. Pip may still install dependencies required by that missing package.

Solver-availability checks and optimal-termination checks remain. Package presence alone does not prove that a solver, licence or future API change will work. An import or compatibility error should be investigated, not hidden by an automatic forced upgrade or downgrade. Exact versions remain in the isolated maintenance test profiles; a classroom constraint should be introduced only for a demonstrated incompatibility.

For local Jupyter use, install the dependencies in a separate environment. The [maintenance baseline](../requirements-test.txt) covers the routine core notebooks, not the optional map lesson or specialist advanced cases; students using Colab should not install that full list over Colab's existing environment.

## Maintenance policy

1. Keep learner setup specific to the notebook: use compatible preinstalled libraries, and install only missing packages or versions required by a documented compatibility issue. Keep the Colab and Binder badges together and keep setup visible and understandable.
2. Keep explicit solver-availability/termination checks in optimization lessons. Use the runtime's installed packages; do not assume Pyomo or HiGHS is absent from Colab. Keep exact baseline versions in maintenance requirements, not learner setup.
3. Keep maintenance pins in an isolated test environment. Do not replace Colab's complete scientific stack simply to match that environment.
4. Run both test profiles, including installation cells, and check dependency conflicts. A final classroom check should also use a fresh actual Colab browser session.
5. Update development course selections as material improves. The historical `v2026.1` checkpoint can remain for provenance; it does not freeze the forthcoming course. Agree and record the final annual edition before distribution.

## What the checks establish

The [execution checker](../scripts/check_resources.py) runs fresh kernels using temporary copies. With `--execute --run-setup`, it runs the conditional dependency cells as well as the lesson; without `--run-setup`, it skips cells tagged `package-install` while retaining lesson imports. [Setup tests](../tests/test_setup.py) also exercise the all-installed and one-missing branches without contacting a package index.

Automated checks cover the [maintenance baseline](../requirements-test.txt) and a [Colab-library compatibility profile](../requirements-colab-test.txt). The latter matches the relevant scientific-library versions in Google's 2026.07 CPU snapshot, not every package or operating-system detail of Colab. Neither profile alone establishes that the browser experience or live map services work. A final check in a fresh actual Colab session remains appropriate before classroom distribution.
