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
        Z: np.ndarray, resid: np.ndarray, inv_S: np.ndarray,
        L: int, K: int) -> TestResult:

    if L < K + 1:
        raise ValueError(f"Model is not overidentified L={L} < K={K} + 1")

    N_T = resid.shape[0]
    scale = Z.T@resid

    statistic = ((scale.T@inv_S@scale) / np.square(N_T))[0][0]

    return statistic, 1-chi2.cdf(statistic, df=L-K)


def pesaran_cd(cc_matrix: np.ndarray, N: int, T: int) -> TestResult:
    """
    Test for cross-sectional dependence based on the cross-sectional matrix
    """

    lower_triang = np.tril(cc_matrix, k=-1)

    scaling_fac = np.sqrt(2*T / (N*(N-1)))

    statistic = scaling_fac*np.sum(lower_triang)

    return statistic, 1-norm.cdf(statistic)


def hausman_test(
    coeff_wg, coeff_gmm,
    v_wg, v_gmm) -> TestResult:

    K = coeff_wg.shape[0]

    diff = coeff_wg - coeff_gmm

    var = inv(v_gmm - v_wg)

    statistic = (diff.T@var@diff)[0][0]

    return statistic, 1-chi2.cdf(statistic, df=K)