from hpl_solver import handle_request
import plotly.io as pio

params = {
    "C": 0.01,
    "g_Na": 4e-2,
    "E_Na": 50,
    "E_K": 85,
    "g_Nac": 3e-5,
    "g_s": 9e-4,
    "m_scaler": 1.0,
    "IstimStart": 0,
    "IstimEnd": 1e42,
    "IstimAmplitude": 0.1,
    "IstimPeriod": 500,
    "IstimPulseDuration": 5,
}

u_0 = {
    "V": -85.0,
    "h": 0.011,
    "m": 0.998,
    "j": 0.975,
    "Cai": 1e-4,
    "d": 0.003,
    "f": 0.994,
    "x1": 0.0001,
}

solver_params = {"t_span": [0, 2000], "method": "LSODA", "max_step": 0.5}
request = dict(
    problem="beeler_reuter",
    parameters=params,
    states=u_0,
    solver_parameters=solver_params,
)
response = handle_request(request)
if response["status"] != "done":
    print(response)
else:
    fig_dict = response["figures"][0]
    pio.show(fig_dict)
