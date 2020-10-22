import numpy as np

from itertools import permutations


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


def cross_correlation(resid: np.ndarray) -> np.ndarray:
    """
    Takes the TxN residual matrix and computes the cross country correlation matrix
    """

    N = resid.shape[1]
    cc_matrix = np.zeros((N, N))

    for i in range(N):
        cc_matrix[i, i] = resid[:, i].T@resid[:, i]

    pairs = permutations(range(N), 2)

    for i, j in pairs:

        country_i = resid[:, i]
        country_j = resid[:, j]

        cross_rho = country_i.T@country_j

        cc_matrix[i, j] = cross_rho
        cc_matrix[j, i] = cross_rho

    return cc_matrix
