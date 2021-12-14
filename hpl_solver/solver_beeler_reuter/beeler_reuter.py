import pandas as pd
from typing import List
import scipy.integrate as scin
from hpl_solver.solver_beeler_reuter.model import calculate_rates, a_syms
from hpl_solver.solver_beeler_reuter.beeler_reuter_parameters import (
    InputStates,
    InputParameters,
    SolverParameters,
)
import plotly.express as px


def draw(solution: pd.DataFrame) -> List[dict]:
    fig = px.line(solution, x="t", y="V")
    fig_dict = fig.to_dict()
    return [fig_dict]


def solve(
    p: InputParameters, y0: InputStates, solver_params: SolverParameters
) -> pd.DataFrame:

    a = dict.fromkeys(a_syms, 0)
    u0 = list(y0.values())
    u_keys = list(y0.keys())

    t_span = solver_params.t_span
    method = solver_params.method
    max_step = solver_params.max_step

    res = scin.solve_ivp(
        calculate_rates,
        t_span=t_span,
        y0=u0,
        method=method,
        max_step=max_step,
        args=[p, a, u_keys],
    )
    solution = pd.DataFrame(res.y.T, columns=u_keys)
    solution["t"] = res.t

    return solution
