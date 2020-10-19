import numpy as np


def autocorrelation(e: np.ndarray) -> np.ndarray:
    """
    Takes the TxN residual matrix and computes the autocorrelation vector
    """

    T = e.shape[0]

    rho = np.empty(T)

    for lag in range(T):
        rho_l = 0
        for t in range(lag, T):
            cov = e[t].T@e[t - lag]
            rho_l += cov

        rho[lag] = rho_l

    return rho
