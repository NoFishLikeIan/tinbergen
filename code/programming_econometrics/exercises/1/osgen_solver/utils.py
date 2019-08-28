import numpy as np
from functools import wraps


def check_shape_inputs(estimating_fn):

    @wraps(estimating_fn)
    def inner(*args, **kwdargs):
        observations = args[0].shape[0]
        if any((a.shape[0] != observations for a in args)):
            raise ValueError('Incompatible sample size between X and y')

        return estimating_fn(*args, **kwdargs)
    return inner


def factored_inverted(matrix):
    '''
    Computes, for M, (M.T @ M)^-1
    '''
    return np.linalg.inv(matrix.T @ matrix)


def compute_variance(estimates, n, k):
    e = estimates.copy().reshape(-1, 1)
    return (e.T @ e) / (n - k)


def compute_residuals(X, y, beta):
    column_y = y.copy().reshape(-1, 1)
    est = column_y - X @ beta
    variance = compute_variance(est, *column_y.shape)
    return variance * factored_inverted(X)


def compute_s(X, y, beta):
    res = compute_residuals(X, y, beta)
    diag = np.diagonal(res)
    return diag ** 1/2
