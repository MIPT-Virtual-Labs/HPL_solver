from typing import List, Optional
from pydantic import BaseModel, ValidationError, validator
from hpl_solver import beeler_reuter  # , restitution


class Error(BaseModel):
    error: str
    field: str


class Response(BaseModel):
    errors: Optional[List[Error]]
    description: Optional[str]
    solution: Optional[dict]
    status: str

    @validator("status")
    def validate_status(cls, st, values):
        if st == "error":
            if "errors" not in values:
                raise ValueError("status is set to `error` but no errors provided")
        else:
            if "errors" in values and values["errors"]:
                raise ValueError(f"status is not {st} but errors were found")
        if st == "failed" and "description" not in values:
            raise ValueError("status is set to `failed` but no description provided")
        return


def handle_request(request_json: dict) -> dict:

    if "problem" not in request_json:
        errors = [Error(error="Specify the problem", field="problem")]
        response = Response(status="error", errors=errors)
        return response.dict()

    problem_name = request_json["problem"]
    problems = {
        "beeler_reuter": beeler_reuter,
        # "restitution": restitution
    }

    if problem_name not in problems:
        errors = [Error(error=f"Unknown problem: `{problem_name}`", field="problem")]
        response = Response(status="error", errors=errors)
        return response.dict()

    solver = problems[problem_name]
    parameters = request_json["parameters"]
    states = request_json["states"]
    solver_parameters = request_json["solver_parameters"]

    try:
        p = solver.InputParameters(**parameters)
        y0 = solver.InputStates(**states)
        solver_params = solver.SolverParameters(**solver_parameters)
    except ValidationError as ve:
        errors = [Error(error=e["msg"], field=e["loc"][0]) for e in ve.errors()]
        response = Response(status="error", errors=errors)
        return response.dict()

    try:
        solution_dict = solver.solve(p, y0, solver_params)
    except Exception as e:
        response = Response(status="failed", description=str(e))
        return response.dict()

    response = Response(status="done", solution=solution_dict)
    response_dict = response.dict()
    return response_dict
