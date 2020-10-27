import numpy as np

from numpy.linalg import inv

from typing import Tuple, NewType

Dim = NewType("Dim", Tuple[int, int])


def white_var(X: np.ndarray, e: np.ndarray, *var_args) -> np.ndarray:

    inverse = inv(X.T@X)

    # construct diagonal array
    omega = np.diag(np.diag(e@e.T))

    var_matrix = X.T@omega@X

    return inverse@var_matrix@inverse

# TODO: The two white can be abstracted

def white_var_2sls(W: np.ndarray, Z: np.ndarray, e: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:

    N_T, K = W.shape

    omega = np.diag(np.diag(e@e.T))
    S_hat = (Z.T@omega@Z) / N_T

    inv_Z = inv(Z.T@Z)

    inverse = inv(W.T@Z@inv_Z@Z.T@W)
    central = W.T@Z@inv_Z@S_hat@inv_Z@Z.T@W
    
    return N_T*(inverse@central@inverse), S_hat


def k(l, m):
    """
    K weighting filter
    """

    return 1 - l/(m+1)


def nw_corrected(stacked_X: np.ndarray, e: np.ndarray, dimensions: Dim) -> np.ndarray:

    N, T = dimensions
    X = stacked_X.reshape(T, N, -1, order="F")
    residuals = e.reshape(T, N, order="F")

    inverse = inv(stacked_X.T@stacked_X)

    gamma_zero = (stacked_X.T@e)@(stacked_X.T@e).T

    M = T - 1

    cov = gamma_zero.copy()

    # TODO: Broadcast in linear algebra
    for lag in range(M):
        weight = k(lag, M)

        gamma_lag = np.zeros(cov.shape)

        for i in range(N):
            for t in range(T):
                lagged_t = t - lag
                lagged_X = X[lagged_t, i].reshape(1, -1)

                squared_resid = residuals[t, i]*residuals[lagged_t, i]
                scale_reg = X[t, i].reshape(-1, 1)@lagged_X
                gamma_lag += squared_resid*scale_reg

        cov += gamma_lag*weight

    return inverse@cov@inverse
