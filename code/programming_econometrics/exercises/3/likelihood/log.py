import numpy as np

from .cond_math import log2pi


def error(y, X, betas):
    e = y - X @ betas
    return e


def log_ll_regression(y, X, parameters):
    """
    Computes the log likelihood of a given observation given a set of parameters

    Parameters
    ----------
    y : Vector[number]
        Observation

    X : Matrix[number]
        Indipendent variables

    parameters : Vector[number]
        Vector of parameters, e.g. [sigma, beta_1, beta_2...]

    Returns
    -------
    Vector[number]
        Log-likelihood of every observation
    """
    [sigma, *betas] = parameters

    errors = error(y, X, betas) / sigma
    log_var = np.log(sigma**2)

    ll_vector = -0.5 * (log2pi + log_var + np.square(errors))

    return ll_vector
