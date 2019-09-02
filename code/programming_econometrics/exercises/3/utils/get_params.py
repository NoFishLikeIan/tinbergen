import numpy as np


def params_to_sigbeta(params):
    return params[0], params[1:]


def compose_params(sigma, betas):
    return np.array([sigma, *betas])
