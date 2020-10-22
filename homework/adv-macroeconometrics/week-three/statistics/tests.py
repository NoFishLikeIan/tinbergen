import numpy as np

from numpy.linalg import inv
from scipy.stats import chi2, norm

from typing import Tuple, NewType

TestResult = NewType("TestResult", Tuple[np.float, np.float])


def panel_dw(resid: np.ndarray) -> TestResult:

    N, T = resid.shape

    variance = np.sum(np.square(resid))

    n_sum = np.empty((T-1, N))

    for t in range(1, T):
        n_sum[t-1] = np.square(resid[:, t] - resid[:, t-1])

    # FIXME: Find the p-value
    return np.sum(n_sum) / variance, None


def overident_restr(
        Z: np.ndarray, resid: np.ndarray, omega: np.ndarray,
        L: int, K: int) -> TestResult:

    scale = Z.T@resid
    var = inv(Z.T@omega@Z)

    statistic = (scale.T@var@scale)[0][0]

    return statistic, 1-chi2.cdf(statistic, df=L-K)


def pesaran_cd(cc_matrix: np.ndarray, N: int, T: int) -> TestResult:
    """
    Test for cross-sectional dependence based on the cross-sectional matrix
    """

    lower_triang = np.tril(cc_matrix, k=-1)

    scaling_fac = np.sqrt(2*T / (N*(N-1)))

    statistic = scaling_fac*np.sum(lower_triang)

    return statistic, 1-norm.cdf(statistic)
