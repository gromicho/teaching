"""Small teaching utilities. Importing this module never installs or solves anything.

Lessons that explain these operations show their implementations; other notebooks
import them. Package installation remains an explicit action at the lesson stage
where that dependency is introduced.
"""
from importlib import metadata
import importlib.util
from pathlib import Path
import os
import subprocess
import sys


def installed_packages():
    """Return installed distribution names and versions, sorted by name."""
    return dict(sorted(
        ((dist.metadata['Name'], dist.version) for dist in metadata.distributions()
         if dist.metadata['Name']), key=lambda item: item[0].casefold()))


def ensure_packages(required_packages):
    """Install only missing imports using this kernel's Python; never upgrade."""
    missing = [package for name, package in required_packages.items()
               if importlib.util.find_spec(name) is None]
    if missing:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *missing])
    return missing


def coin_solver_directory():
    """Locate an already installed AMPL COIN module, without installing it."""
    spec = importlib.util.find_spec('ampl_module_coin')
    if spec is None:
        return None
    return Path(spec.origin).parent / 'bin'


def install_coin_solvers():
    """Explicitly install the open-source Ipopt/CBC binaries from AMPL's index.

    https://dev.ampl.com/ampl/python/modules.html documents their use with Pyomo.
    No remote solve, licence activation or system-wide installer is invoked.
    """
    if importlib.util.find_spec('ampl_module_coin') is None:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-q',
            '--index-url', 'https://pypi.ampl.com', 'ampl_module_coin'])
    directory = coin_solver_directory()
    if directory is None or not directory.is_dir():
        raise RuntimeError('The COIN solver module did not provide a bin directory.')
    return directory


def make_solver(name):
    """Construct a Pyomo solver; find COIN binaries without changing PATH."""
    import pyomo.environ as pyo
    if name in {'ipopt', 'cbc', 'bonmin', 'couenne'}:
        directory = coin_solver_directory()
        if directory is not None:
            executable = directory / (name + ('.exe' if os.name == 'nt' else ''))
            if executable.is_file():
                # AMPL's CBC binary speaks the NL/ASL protocol, not the command
                # language of the standalone CBC shell plugin.
                interface = 'cbcnl' if name == 'cbc' else name
                return pyo.SolverFactory(interface, executable=str(executable))
    return pyo.SolverFactory(name)


def available_pyomo_solvers(candidates=None):
    """Check named interfaces, not solver licences or mathematical capabilities.

    The default is a course-oriented selection, not every Pyomo plugin.
    Two interfaces such as highs/appsi_highs are the same solver engine.
    """
    if candidates is None:
        candidates = ('appsi_highs', 'highs', 'ipopt', 'cbc', 'glpk',
                      'gurobi_direct', 'cplex_direct', 'mosek', 'scip', 'xpress')
    result = {}
    for name in candidates:
        try:
            result[name] = bool(make_solver(name).available(exception_flag=False))
        except (ImportError, RuntimeError, ValueError, AttributeError):
            result[name] = False
    return result


def reset_model(model):
    """Clear unfixed variable values, including variables inside nested blocks.

    This does not clear a persistent solver's state. For independent timings,
    create a fresh model and solver for every run.
    """
    import pyomo.environ as pyo
    for variable in model.component_data_objects(pyo.Var, descend_into=True):
        if not variable.fixed:
            variable.set_value(None)


def solve_checked(model, solver_name='appsi_highs', **kwargs):
    """Solve and require optimal termination before returning a result."""
    import pyomo.environ as pyo
    solver = make_solver(solver_name)
    if not solver.available(exception_flag=False):
        raise RuntimeError(f'Required solver {solver_name!r} is unavailable.')
    result = solver.solve(model, **kwargs)
    pyo.assert_optimal_termination(result)
    return result
