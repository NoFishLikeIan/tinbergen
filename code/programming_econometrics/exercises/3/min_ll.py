import math
import numpy as np

from likelihood.log import log_ll_regression


def identity(a):
    return a


def average_ll_reg(parameters, y, X, transforming_fn):
    p_prime = transforming_fn(parameters)
    ll = log_ll_regression(y, X, p_prime)
    return - np.mean(ll)
