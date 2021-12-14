from typing import Optional, Tuple

from pydantic import BaseModel


class OdeSolverOptions(BaseModel):
    t_span: Tuple[float, float]
    method: str
    max_step: Optional[float] = 0.1
