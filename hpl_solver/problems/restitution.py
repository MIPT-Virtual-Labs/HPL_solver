import logging
from typing import List

import plotly.graph_objects as go

from hpl_solver.problems import multiple_runs

from . import multiple_runs
from .single_run import SingleRunArgs

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def draw(solutions: list) -> List[dict]:

    logger.debug("draw")

    fig = go.Figure()

    for solution in solutions:
        logger.debug("add trace")

        fig.add_trace(go.Scatter(x=solution["t"], y=solution["V"], name=solution["CL"]))

    logger.debug("add update_layout")

    fig.update_layout(
        title="Last beat",
        xaxis_title="t, ms",
        yaxis_title="V, mV",
        legend_title="Pacing Cycle Length, ms",
    )

    logger.debug("return json")
    fig_json = fig.to_json()
    return [fig_json]


def filter_solution(solution, t_start, t_end):

    logger.debug("filter")
    solution_filtered = {key: [] for key in solution}
    solution_t = solution["t"]

    for i, t in enumerate(solution_t):
        if t_start <= t <= t_end:
            for key in solution:
                solution_filtered[key].append(solution[key][i])

    solution_filtered["t"] = [t - t_start for t in solution_filtered["t"]]

    return solution_filtered


def solve(args: List[SingleRunArgs]) -> list:

    solutions = multiple_runs.solve(args)
    solutions_filtered = []

    for arg, solution in zip(args, solutions):

        CL = arg["parameters"]["IstimPeriod"]
        t_last = solution["t"][-1]

        t_start = ((t_last // CL) - 2) * CL - 10
        t_end = t_start + 600

        solution_filtered = filter_solution(solution, t_start, t_end)
        solutions_filtered.append(solution_filtered)
        solution_filtered["CL"] = CL

    logger.debug("solved")
    return solutions_filtered
