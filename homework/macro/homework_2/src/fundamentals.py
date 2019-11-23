import numpy as np


def max_prod_function(k, alpha):
    return np.power(k, alpha)


def gamma_c(w, phi):
    return np.power(w, 1 + phi)


def gamma_e(w, phi):
    return w - gamma_c(w, phi)


def make_u(epsilon, phi):
    def apply(coords):
        c, e = coords
        if np.isinf(e):
            return -np.inf

        w = c + e
        positive = np.sqrt(w)

        negative = np.power(c - gamma_c(w, phi), 2) + \
            np.power(e - gamma_e(w, phi), 2)

        return positive - epsilon * negative

    return apply
