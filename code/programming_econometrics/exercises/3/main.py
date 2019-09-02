import numpy as np
import pandas as pd
import scipy.optimize as opt

from constants import X, betas, sigma, l

from simulate.generate import gen_ys
from likelihood.log import log_ll_regression


def transform(parameters):
    ps = parameters.copy()
    ps[0] = np.log(parameters[0])
    return ps


def invert(parameters):
    ps = parameters.copy()
    ps[0] = np.exp(parameters[0])
    return ps


def main():
    y = gen_ys(X, betas, sigma, l)

    parameters = np.array([sigma, *betas])

    paramaters_init = np.ones(parameters.shape) * 2

    result = opt.minimize(
        lambda parameters: - np.mean(log_ll_regression(y, X, parameters)),
        paramaters_init,
        method='BFGS'
    )

    [sigma_hat, *betas_hat] = np.copy(result.x)

    print('Actual:', sigma, betas)
    print('Estimated:', sigma_hat, betas_hat)


if __name__ == '__main__':
    main()
