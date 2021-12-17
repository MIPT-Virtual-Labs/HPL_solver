from copy import deepcopy

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
    "IstimPeriod": 1000,
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
solver_options = {"t_span": [0, 10_000], "method": "LSODA", "max_step": 0.5}

args_base = dict(
    model_name=model_name,
    states=states,
    parameters=parameters,
    solver_options=solver_options,
)

CLs = [2000, 1333, 1000, 666, 500, 333]
args_list = []

for CL in CLs:

    args = deepcopy(args_base)
    args["parameters"]["IstimPeriod"] = CL
    args_list.append(args)

request = dict(problem="multiple_runs", args=args_list)

response = handle_request(request)

import json

# with open("tmp.json", "w") as f:
#     f.write(json.dumps(response))

if response["status"] != "done":
    print(response)
else:
    for fig_json in response["figures"]:
        fig_dict = json.loads(fig_json)
        pio.show(fig_dict)
