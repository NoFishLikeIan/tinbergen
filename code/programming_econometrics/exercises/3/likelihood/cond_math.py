import numpy as np

log2pi = np.log(2 * np.pi)


def log2pi_vector(shape):
    return np.ones(shape) * log2pi
