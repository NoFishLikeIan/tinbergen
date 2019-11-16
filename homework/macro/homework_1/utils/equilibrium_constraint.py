import numpy as np


def budget_constraint(v_1, sigma_1, sigma_2, pH):
    exp = (sigma_1 - 1) / sigma_1
    return v_1 + np.power(pH, exp) * v_1 - pH
