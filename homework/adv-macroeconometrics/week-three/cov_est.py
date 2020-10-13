import numpy as np

from typing import Tuple, NewType

Dim = NewType("Dim", Tuple[int, int])

def white_var(X: np.ndarray, e: np.ndarray, dimensions: Dim) -> np.ndarray:
    inverse = np.linalg.inv(X.T@X)
    
    # construct diagonal array
    diag = np.diag(np.diag(e@e.T))
    
    var_matrix = X.T@diag@X
    
    return inverse@var_matrix@inverse


def nw_corrected(X: np.ndarray, e: np.ndarray, dimensions: Dim) -> np.ndarray:
    inverse = np.linalg.inv(X.T@X)

    N, T = dimensions
    residuals = e.reshape(T, N)
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
                sqrd_res = residuals[t, i]*residuals[t - past_lag, i]
                coproduct = res_X[t, i].T@res_X[t - past_lag, i]

                gamma_l += sqrd_res*coproduct

        lagged += weight* (gamma_l + gamma_l.T)

    breakpoint()
    return