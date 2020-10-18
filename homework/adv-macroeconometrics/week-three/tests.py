import numpy as np

from numpy.linalg import inv
from scipy.stats import chi2

from typing import Tuple


def panel_dw(resid: np.ndarray, N: int, T: int) -> np.float:

    variance = np.sum(np.square(resid))

    n_sum = np.empty((T-1, N))

    for t in range(1, T):
        n_sum[t-1] = np.square(resid[t] - resid[t-1])

    return np.sum(n_sum) / variance


def overident_restr(
    Z: np.ndarray, resid: np.ndarray, omega: np.ndarray,
    L: int, K: int
) -> Tuple[np.float, np.float]:

    scale = Z.T@resid
    var = inv(Z.T@omega@Z)

    statistic = (scale.T@var@scale)[0][0]

    return statistic, chi2.cdf(statistic, df=L-K)
