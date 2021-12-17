import logging
from typing import List

import numpy as np
import plotly.graph_objects as go

from hpl_solver.problems import multiple_runs

from . import multiple_runs
from .single_run import SingleRunArgs

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def draw_waveforms(solutions: list) -> str:
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

    return fig_json


def draw_restitution_curve(solutions: list) -> str:
    logger.debug("draw")

    CLs = [s["CL"] for s in solutions]
    APDs = [s["APD"] for s in solutions]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=CLs, y=APDs))

    logger.debug("add update_layout")

    fig.update_layout(
        title="Restitution curve",
        xaxis_title="Pacing Cycle Length, ms",
        yaxis_title="Action Potential Duration 80, ms",
    )

    logger.debug("return json")
    fig_json = fig.to_json()

    return fig_json


def draw(solutions: list) -> List[str]:
    return [draw_waveforms(solutions), draw_restitution_curve(solutions)]


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

        APD = calculate_APD(solution_filtered["t"], solution_filtered["V"])
        solution_filtered["CL"] = CL
        solution_filtered["APD"] = APD

    logger.debug("solved")
    return solutions_filtered


def calculate_APD(time, signal, percentage=80.0):
    """ Calculate Action Potential Duration for ``percentage`` level repolarization of the ``signal``.

    Parameters
    ----------
    ``time`` : np.ndarray, shape=(T)
    ``signal`` : np.ndarray, shape=(T)
    ``percentage`` : float, optional
        level of signal to calculate duration (default is 80)

    Returns
    -------
    float or np.NaN
        APD in time units of ``time``
    """

    time_copy, signal_copy = map(np.array, (time, signal))

    if not (0 < percentage < 100):
        msg = "percentage must be in range (0, 100) but {} was given".format(percentage)
        raise Exception(msg)

    index = np.nonzero(
        signal_copy < signal_copy.min() + (1.0 - percentage / 100.0) * signal_copy.ptp()
    )
    index = index[0]
    spaces = time_copy[index[1:]] - time_copy[index[:-1]]
    if len(spaces):
        APD = np.nanmax(spaces)
    else:
        APD = np.NaN
    return APD
