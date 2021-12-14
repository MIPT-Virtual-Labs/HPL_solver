import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import numpy as np


def calculate_alpha_m(V):
    alpha_m = -1.0 * (V + 47.0) / (np.exp(-0.1 * (V + 47.0)) - 1)
    return alpha_m


def calculate_beta_m(V):
    beta_m = 40.0 * np.exp(-0.056 * (V + 72.0))
    return beta_m


def calculate_alpha_h(V):
    alpha_h = 0.126 * np.exp(-0.25 * (V + 77.0))
    return alpha_h


def calculate_beta_h(V):
    beta_h = 1.7 / (1 + np.exp(-0.082 * (V + 22.5)))
    return beta_h


def calculate_alpha_j(V):
    alpha_j = 0.055 * np.exp(-0.25 * (V + 78.0)) / (1.0 + np.exp(-0.2 * (V + 78.0)))
    return alpha_j


def calculate_beta_j(V):
    beta_j = 0.3 / (1.0 + np.exp(-0.1 * (V + 32.0)))
    return beta_j


def calculate_alpha_d(V):
    alpha_d = 0.095 * np.exp(-(V - 5.0) / 100.0) / (1.0 + np.exp(-(V - 5.0) / 13.89))
    return alpha_d


def calculate_beta_d(V):
    beta_d = 0.07 * np.exp(-(V + 44.0) / 59.0) / (1.0 + np.exp((V + 44.0) / 20.0))
    return beta_d


def calculate_alpha_f(V):
    alpha_f = 0.012 * np.exp(-(V + 28.0) / 125.0) / (1.0 + np.exp((V + 28.0) / 6.67))
    return alpha_f


def calculate_beta_f(V):
    beta_f = 0.0065 * np.exp(-(V + 30.0) / 50.0) / (1.0 + np.exp(-(V + 30.0) / 5.0))
    return beta_f


def calculate_alpha_x1(V):
    alpha_x1 = 5e-4 * np.exp((V + 50.0) / 12.1) / (1.0 + np.exp((V + 50.0) / 17.5))
    return alpha_x1


def calculate_beta_x1(V):
    beta_x1 = 0.0013 * np.exp(-(V + 20.0) / 16.67) / (1.0 + np.exp(-(V + 20.0) / 25.0))
    return beta_x1


def calculate_E_s(u, p, t, a):
    a["E_s"] = -82.3 - (13.0287 * np.log(u["Cai"] * 0.001))


def calculate_i_s(u, p, t, a):
    a["i_s"] = p.g_s * u["d"] * u["f"] * (u["V"] - a["E_s"])


def calculate_i_Na(u, p, t, a):
    a["i_Na"] = (p.g_Na * u["m"] ** 3 * u["h"] * u["j"] + p.g_Nac) * (u["V"] - p.E_Na)


def calculate_i_x1(u, p, t, a):
    a["i_x1"] = (
        u["x1"]
        * 8e-3
        * (np.exp(0.004 * (u["V"] + 77.0)) - 1.0)
        / (np.exp(0.04 * (u["V"] + 35.0)))
    )


def calculate_i_K1(u, p, t, a):
    a["i_K1"] = 0.0035 * (
        4.0
        * (np.exp(0.04 * (u["V"] + p.E_K)) - 1)
        / (np.exp(0.08 * (u["V"] + 53.0)) + np.exp(0.04 * (u["V"] + 53.0)))
        + 0.2 * (u["V"] + 23.0) / (1 - np.exp(-0.04 * (u["V"] + 23.0)))
    )


def calculate_Istim(u, p, t, a):
    condition = (
        p.IstimStart <= t <= p.IstimEnd
        and (t - p.IstimStart)
        - np.floor((t - p.IstimStart) / p.IstimPeriod) * p.IstimPeriod
        <= p.IstimPulseDuration
    )
    a["Istim"] = p.IstimAmplitude if condition else 0.0
    logger.debug(f"time: {t}, Istim: {a['Istim']}")


def calculate_algebraic(u, p, t, a):
    V = u["V"]

    a["alpha_m"] = calculate_alpha_m(V)
    a["beta_m"] = calculate_beta_m(V)

    a["alpha_h"] = calculate_alpha_h(V)
    a["beta_h"] = calculate_beta_h(V)

    a["alpha_j"] = calculate_alpha_j(V)
    a["beta_j"] = calculate_beta_j(V)

    a["alpha_d"] = calculate_alpha_d(V)
    a["beta_d"] = calculate_beta_d(V)

    a["alpha_f"] = calculate_alpha_f(V)
    a["beta_f"] = calculate_beta_f(V)

    a["alpha_x1"] = calculate_alpha_x1(V)
    a["beta_x1"] = calculate_beta_x1(V)

    calculate_E_s(u, p, t, a)
    calculate_i_s(u, p, t, a)
    calculate_i_Na(u, p, t, a)
    calculate_i_x1(u, p, t, a)
    calculate_i_K1(u, p, t, a)
    calculate_Istim(u, p, t, a)


def calculate_d_gate(gate, alpha, beta, scaler=1):
    d_gate = scaler * (alpha * (1.0 - gate) - beta * gate)
    return d_gate


def calculate_d_Cai(du, u, p, t, a):
    d_Cai = -0.01 * a["i_s"] + 0.07 * (0.0001 - u["Cai"])
    return d_Cai


def calculate_d_V(du, u, p, t, a):
    d_V = (a["Istim"] - (a["i_Na"] + a["i_s"] + a["i_x1"] + a["i_K1"])) / p.C
    return d_V


def calculate_rates(t, u, p, a, u_keys):

    u = dict(zip(u_keys, u))
    du = dict.fromkeys(u_keys, 0)

    calculate_algebraic(u, p, t, a)
    du["m"] = calculate_d_gate(u["m"], a["alpha_m"], a["beta_m"], p.m_scaler)
    du["h"] = calculate_d_gate(u["h"], a["alpha_h"], a["beta_h"])
    du["j"] = calculate_d_gate(u["j"], a["alpha_j"], a["beta_j"])
    du["d"] = calculate_d_gate(u["d"], a["alpha_d"], a["beta_d"])
    du["f"] = calculate_d_gate(u["f"], a["alpha_f"], a["beta_f"])
    du["x1"] = calculate_d_gate(u["x1"], a["alpha_x1"], a["beta_x1"])

    du["V"] = calculate_d_V(du, u, p, t, a)
    du["Cai"] = calculate_d_Cai(du, u, p, t, a)

    du = np.array(list(du.values()))

    return du
