import numpy as np


def consumptions(v, pH, sigma_1, sigma_2):

    return (v, v * np.power(pH, -1/sigma_1))
