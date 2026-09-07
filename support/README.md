# Shared teaching utilities

`teaching_utils.py` provides `installed_packages`, `ensure_packages`, `available_pyomo_solvers`, `make_solver`, `reset_model` and `solve_checked`. The explicit `install_coin_solvers` function installs the open-source Ipopt/CBC binaries when a lesson requests them. Importing the module has no installation side effects.

Notebooks in a checkout find `support/` locally. Standalone Colab notebooks retrieve a hash-verified copy. Utility explanations show the implementation; ordinary users import it. See the [solver-environment lesson](../courses/aabw/notebooks/lecture-2/jeff-kantor-solver-installation.ipynb).

Solver availability is a preliminary interface check, not proof of a usable licence or support for a particular mathematical model. Check actual termination and verify the model's expected result. Use fresh models and solver objects for independent comparisons.

The existing `util_AABW.py` workbook helper remains available for established course examples.
