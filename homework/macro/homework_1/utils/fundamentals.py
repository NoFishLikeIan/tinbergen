import numpy as np


def consumptions(v, pH, sigma_1, sigma_2):
    return (v, v * np.power(pH, -1/sigma_1))


def utility(low_c, high_c, sigma, beta=0.95):
    risk_factor = 1 - sigma
    discount_factor = beta / (1 - beta)
    total_factor = 0.5 * (1 / risk_factor) * discount_factor

    c_l, c_h = np.power(low_c, risk_factor), np.power(high_c, risk_factor)

    return (c_l + c_h) * total_factor
