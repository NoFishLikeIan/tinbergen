import numpy as np
import pandas as pd
import scipy.optimize as opt

from constants import X, betas, sigma, l

from simulate.generate import gen_ys
from min_ll import average_ll_reg


def transform(parameters):
    ps = parameters.copy()
    ps[0] = np.log(parameters[0])
    return ps


def invert(parameters):
    ps = parameters.copy()
    ps[0] = np.exp(parameters[0])
    return ps


def minimize(fn, init, y, X, transform, invert):

    result = opt.minimize(fn, transform(init), args=(
        y, X, invert), method='BFGS')

    estimate = invert(result.x)

    return estimate


def main():
    y = gen_ys(X, betas, sigma, l)

    parameters = np.array([sigma, *betas])

    paramaters_init = np.ones(parameters.shape) * 2

    result = minimize(average_ll_reg, paramaters_init, y, X, transform, invert)

    [sigma_hat, *betas_hat] = np.copy(result)

    print('Actual:', sigma, betas)
    print('Estimated:', sigma_hat, betas_hat)


if __name__ == '__main__':
    main()
