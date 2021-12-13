from numpy.core.fromnumeric import _take_dispatcher
from hpl_solver import handle_request, solver_beeler_reuter

params = {"C": 0.01,
        "g_Na" : 4e-2,
        "E_Na" : 50,
        "E_K" : 85,
        "g_Nac" : 3e-5,
        "g_s" : 9e-4,
        "m_scaler" : 1.,
        "IstimStart" : 0,
        "IstimEnd" : 50000,
        "IstimAmplitude" : 0.5,
        "IstimPeriod" : 1000,
        "IstimPulseDuration" : 1}

u_0 = {"V" : -85.0,
       "h" : 0.011,
       "m" : 0.998,
       "j" : 0.975,
       "Cai" : 1e-4,
       "d" : 0.003,
       "f" : 0.994,
       "x1" : 0.0001}

solver_params ={
        "t_span":[0, 500],
        'method':"LSODA"
} 
request = dict(problem="beeler_reuter", parameters=params, states = u_0, solver_parameters = solver_params)
response = handle_request(request)
print(response)
