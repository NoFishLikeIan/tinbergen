import math
import numpy as np

from likelihood.log import log_ll_regression


def bounded_mean_ll(parameters, y, X, verbose=0):
    [sigma, *_] = parameters

    if verbose > 0:
        print('Sigma: ', sigma)
        print('Betas: ', _)

    if sigma < 0:
        res = math.inf
    else:
        ll_vector = log_ll_regression(y, X, parameters)
        res = -1 * np.mean(ll_vector)

    if verbose > 0:
        print('Mean neg. log lik.:', res)
        print('\n')

    return res
