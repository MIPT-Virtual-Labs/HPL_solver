import logging
from typing import List

import pandas as pd
import plotly.express as px
from pydantic import BaseModel, validator
from scipy.integrate import solve_ivp

from hpl_solver.models import beeler_reuter

from ..ode_solver_options import OdeSolverOptions

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

models = {"beeler_reuter": beeler_reuter}


class SingleRunArgs(BaseModel):
    model_name: str
    states: dict
    parameters: dict
    solver_options: OdeSolverOptions

    @validator("model_name")
    def model_is_implemented(cls, model_name):
        if model_name not in models:
            raise ValueError(f"Model {model_name} is not implemented")
        return model_name


def draw(solution: dict) -> List[dict]:
    logger.debug("start")
    df = pd.DataFrame(solution)
    fig = px.line(df, x="t", y="V")
    fig_dict = fig.to_dict()
    return [fig_dict]


def solve(args: dict) -> pd.DataFrame:

    logger.debug("problem is started")

    args = SingleRunArgs(**args)
    model = models[args.model_name]
    states = model.States(**args.states)
    parameters = model.Parameters(**args.parameters)
    algebraics = model.Algebraics().dict()
    y0 = list(states.dict().values())
    states_keys = list(states.dict().keys())

    logger.debug("problem is prepared")

    res = solve_ivp(
        model.calculate_rates,
        t_span=args.solver_options.t_span,
        y0=y0,
        method=args.solver_options.method,
        max_step=args.solver_options.max_step,
        args=[parameters, algebraics, states_keys],
    )

    solution = dict(zip(states_keys, res.y))
    solution["t"] = res.t

    return solution
