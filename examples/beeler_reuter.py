import json

import plotly.io as pio

from hpl_solver import handle_request

parameters = {
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

states = {
    "V": -85.0,
    "h": 0.011,
    "m": 0.998,
    "j": 0.975,
    "Cai": 1e-4,
    "d": 0.003,
    "f": 0.994,
    "x1": 0.0001,
}

model_name = "beeler_reuter"
solver_options = {"t_span": [0, 2000], "method": "LSODA", "max_step": 0.5}
request = dict(
    problem="single_run",
    args=dict(
        model_name=model_name,
        states=states,
        parameters=parameters,
        solver_options=solver_options,
    ),
)
response = handle_request(request)
if response["status"] != "done":
    print(response)
else:
    for fig_json in response["figures"]:
        fig_dict = json.loads(fig_json)
        pio.show(fig_dict)
