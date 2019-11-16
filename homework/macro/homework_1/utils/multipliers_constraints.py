import numpy as np


def high_constraint(v_1, sigma_1, sigma_2, price):
    first = np.power(price, -1/sigma_1) * v_1
    second = np.power(price, -1/sigma_2) * (1 - v_1)

    return first + second
