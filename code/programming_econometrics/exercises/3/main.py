import numpy as np
import pandas as pd
import scipy.optimize as opt

from constants import X, betas, sigma, l

from simulate.generate import gen_ys
from min_ll import bounded_mean_ll


def main():
    np.random.seed(11148705)
    y = gen_ys(X, betas, sigma, l)

    parameters = np.array([sigma, *betas])

    # bounded_mean_ll(parameters, y, X, verbose=True)

    result = opt.minimize(bounded_mean_ll,
                          parameters,
                          args=(y, X, 0),
                          method='BFGS')

    print(result)


if __name__ == '__main__':
    main()
