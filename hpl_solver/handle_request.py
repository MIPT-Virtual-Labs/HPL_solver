from pydantic import ValidationError

from .problems import multiple_runs, single_run
from .response import Error, Response


def handle_request(request_json: dict) -> dict:

    if "problem" not in request_json:
        errors = [Error(error="Specify the problem", field="problem")]
        response = Response(status="error", errors=errors)
        return response.dict()

    problem_name = request_json["problem"]

    problems = {"single_run": single_run, "multiple_runs": multiple_runs}

    if problem_name not in problems:
        errors = [Error(error=f"Unknown problem: `{problem_name}`", field="problem")]
        response = Response(status="error", errors=errors)
        return response.dict()

    problem = problems[problem_name]
    args = request_json["args"]

    try:
        solution = problem.solve(args)
        figures = problem.draw(solution)
    except ValidationError as ve:
        errors = [Error(error=e["msg"], field=e["loc"][0]) for e in ve.errors()]
        response = Response(status="error", errors=errors)
        return response.dict()
    except Exception as e:
        response = Response(status="failed", description=str(e))
        return response.dict()

    response = Response(status="done", figures=figures, solution=solution)
    response_dict = response.dict()
    return response_dict
