import logging
import numpy as np
import pandas as pd
import scipy.integrate as scin
from hpl_solver.solver_beeler_reuter.model import calculate_rates, a_syms
from hpl_solver.solver_beeler_reuter.beeler_reuter_parameters import (
    InputStates,
    InputParameters,
    SolverParameters,
)
import plotly.express as px
import json


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def solve(
    p: InputParameters, y0: InputStates, solver_params: SolverParameters
) -> np.ndarray:

    a = dict.fromkeys(a_syms, 0)
    u0 = list(y0.values())
    u_keys = list(y0.keys())

    t_span = solver_params.t_span
    method = solver_params.method

    res = scin.solve_ivp(
        calculate_rates, t_span=t_span, y0=u0, method=method, args=[p, a, u_keys]
    )
    solution = pd.DataFrame(res.y.T, columns=u_keys)
    solution["t"] = res.t

    fig = px.line(solution, x="t", y="V")
    solution_fig = json.loads(fig.to_json(pretty=True))

    return solution_fig
