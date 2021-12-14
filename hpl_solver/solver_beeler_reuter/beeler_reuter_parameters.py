from pydantic import BaseModel, validator, root_validator
from typing import Optional


class InputStates(BaseModel):

    V: float
    m: float
    h: float
    j: float
    Cai: float
    d: float
    f: float
    x1: float

    def values(self):
        return self.__dict__.values()

    def keys(self):
        return self.__dict__.keys()

    @validator("m", "h", "j", "d", "f", "x1")
    def check_gate_bounds(cls, gate):
        lb, ub = 0, 1
        if gate < lb or gate > ub:
            raise ValueError(f"Incorrect value: {gate}, must be in range [{lb}, {ub}]")
        return gate

    @validator("V")
    def check_v_bounds(cls, v):
        lb, ub = -500, 500
        if v < lb or v > ub:
            raise ValueError(f"Incorrect value: {v}, must be in range [{lb}, {ub}]")
        return v


class InputParameters(BaseModel):

    C: float
    g_Na: float
    E_Na: float
    E_K: float
    g_Nac: float
    g_s: float
    m_scaler: float
    IstimStart: float
    IstimEnd: float
    IstimAmplitude: float
    IstimPeriod: float
    IstimPulseDuration: float

    def values(self):
        return self.__dict__.values()

    def keys(self):
        return self.__dict__.keys()

    @root_validator
    def check_Istim(cls, params):
        IstimStart = params.get("IstimStart")
        IstimEnd = params.get("IstimEnd")
        if IstimStart >= IstimEnd:
            raise ValueError(
                f"Parameter 'IstimStart'={IstimStart} should be less than 'IstimEnd'={IstimEnd}"
            )
        return params


class SolverParameters(BaseModel):

    t_span: list
    method: str
    max_step: Optional[float] = 0.1

    @validator("t_span")
    def check_t_span(cls, t):
        lb, ub = t
        if lb >= ub:
            raise ValueError(f"Incorrect value: {t}, {lb} should be smaller than {ub}]")
        return t

    @validator("method")
    def check_method(cls, method):
        method_list = ["RK45", "RK23", "DOP853", "Radau", "BDF", "LSODA"]
        if method not in method_list:
            raise ValueError(
                f"Undefined method : {method}, must be one of the list {method_list}"
            )
        return method
