
import logging
import os
import subprocess
import numpy as np
import pandas as pd
import scipy.integrate as scin
from hpl_solver.solver_beeler_reuter.model import calculate_algebraic, calculate_rates 
from hpl_solver.solver_beeler_reuter.beeler_reuter_parameters import InputStates, InputParameters, SolverParameters
import plotly.express as px


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def solve(p: InputParameters, y0: InputStates, solver_params: SolverParameters ) -> np.ndarray:

    a_syms = ("alpha_m", "beta_m",
            "alpha_h", "beta_h",
            "alpha_j", "beta_j",
            "alpha_d", "beta_d",
            "alpha_f", "beta_f",
            "alpha_x1", "beta_x1",
            "E_s", "i_s", "i_Na", 
            "i_x1", "i_K1", "Istim")

    
    a = dict.fromkeys(a_syms, 0)
    u0 = list(y0.values())
    u_keys = list(y0.keys())

    t_span = solver_params.t_span
    method = solver_params.method

    res = scin.solve_ivp(calculate_rates, t_span = t_span, y0 = u0, method=method, args=[p, a, u_keys])
    solution = pd.DataFrame(res.y.T, columns=u_keys)
    solution["t"] = res.t
    solution_dict = dict(solution)

    return solution_dict