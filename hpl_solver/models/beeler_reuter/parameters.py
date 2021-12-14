from pydantic import BaseModel, root_validator, validator


class States(BaseModel):

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


class Parameters(BaseModel):

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


class Algebraics(BaseModel):
    alpha_m: float = 0.0
    beta_m: float = 0.0
    alpha_h: float = 0.0
    beta_h: float = 0.0
    alpha_j: float = 0.0
    beta_j: float = 0.0
    alpha_d: float = 0.0
    beta_d: float = 0.0
    alpha_f: float = 0.0
    beta_f: float = 0.0
    alpha_x1: float = 0.0
    beta_x1: float = 0.0
    E_s: float = 0.0
    i_s: float = 0.0
    i_Na: float = 0.0
    i_x1: float = 0.0
    i_K1: float = 0.0
    Istim: float = 0.0
