import logging
from typing import List

from . import single_run
from .single_run import SingleRunArgs

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def draw(solution: list) -> List[dict]:
    logger.debug("start")
    figures = [single_run.draw(x)[0] for x in solution]
    logger.debug("end")
    return figures


def solve(args: List[SingleRunArgs]) -> list:

    logger.debug("multiple_runs starts")
    solution = [single_run.solve(x) for x in args]
    return solution
