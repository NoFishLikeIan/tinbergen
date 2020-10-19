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


def white_var_2sls(W: np.ndarray, W_f: np.ndarray, e: np.ndarray, *var_args) -> np.ndarray:

    inverse = inv(W.T@W_f)
    omega = np.diag(np.diag(e@e.T))

    return inverse@W_f.T@omega@W_f@inverse


def nw_corrected(X: np.ndarray, e: np.ndarray, dimensions: Dim) -> np.ndarray:
    inverse = inv(X.T@X)

    N, T = dimensions
    res_X = X.reshape(T, N, -1)

    contemp = (X.T@e)@(X.T@e).T

    lagged = 0
    M = T - 1

    # TODO: Broadcast in linear algebra
    for past_lag in range(M):
        weight = 1 - past_lag/T

        gamma_l = 0

        for i in range(N):
            for t in range(past_lag+1, T):
                sqrd_res = e[t, i]*e[t - past_lag, i]
                coproduct = res_X[t, i].T@res_X[t - past_lag, i]

                gamma_l += sqrd_res*coproduct

        lagged += weight * (gamma_l + gamma_l.T)

    breakpoint()
    return
