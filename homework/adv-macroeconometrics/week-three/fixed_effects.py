import numpy as np
import pandas as pd

from utils import transform, matrix, printing

from statistics.cov_est import white_var, nw_corrected
from statistics.tests import panel_dw, pesaran_cd, TestResult

from utils.residual_transformation import cross_correlation

# --- Typings

from data_types import EstimationResults
from typing import List


def pesaran_pipe(resid: np.ndarray) -> TestResult:

    N, T = resid.shape

    rho = cross_correlation(resid)
    results = pesaran_cd(rho, N, T)

    return results


tests_fns = {
    "Durbin-Watson": panel_dw,
    "Pesaran": pesaran_pipe
}


def ols_estimate(X, Y, N, T):

    beta = np.linalg.inv(X.T@X)@(X.T@Y)
    resid = Y - X@beta
    
    return beta, resid

def within_group(data: pd.DataFrame, dependent: str,
                 regressors: List[str] = [], lags=0,
                 het_robust=False, cross_sec=False,
                 verbose=1, **print_kwargs) -> EstimationResults:

    if len(regressors) == 0:
        regressors = data.index.get_level_values(0).tolist()

    if lags > 0:

        data, lagged_names = transform.make_multi_lagged(
            data, dependent, lags=lags)

        regressors += lagged_names

    # stack the Y variable
    Y, _, _ = matrix.stack_to_columns(data, dependent)
    X, N, T = matrix.stack_to_columns(data, regressors)

    Q = np.kron(np.identity(N), matrix.make_Q(T))

    X_dem = Q@X
    Y_dem = Q@Y

    beta, resid = ols_estimate(X_dem, Y_dem, N, T)
    resid_by_n = resid.reshape(T, N, order="F")

    tests = {
        test_name: fn(resid_by_n) for (test_name, fn) in tests_fns.items()
    }


    if cross_sec:
        # Add dummy for cross-sectionally dependent data
        dummy_matrix = transform.make_dummy(data, regressors, N, T)
        X_with_dummy = np.hstack((X_dem, dummy_matrix))
        # breakpoint()

        dummy_beta, resid = ols_estimate(X_with_dummy, Y, N, T)
        beta = dummy_beta[:len(regressors)]

        resid_by_n = resid.reshape(T, N, order="F")
        # FIXME: This gives same estimate, not right.
    
        
    fixed_effects = resid_by_n.mean(axis=0)

    cov_fn = nw_corrected if het_robust else white_var

    cov = cov_fn(X_dem, resid, (N, T))

    if verbose:
        # Print as a table
        printing.pprint(beta, cov, regressors, tests, **print_kwargs)

    return beta, fixed_effects, resid_by_n, cov, tests


if __name__ == '__main__':
    from utils.ingest import read_data

    data = read_data("data/hw3.xls")

    # partial = data.loc[(slice(None), slice("1981-01-01")),
    #                    ["Australia", "Belgium"]]  # test with few data points

    beta, fixed_effects, resid_by_n, cov, durbin_watson = within_group(
        data, "S/Y", ["d(lnY)", "INF"], lags=0, title="Within estimator")

    if False:


        beta, fixed_effects, resid_by_n, cov, durbin_watson = within_group(
            data, "S/Y", ["d(lnY)", "INF"], lags=1, het_robust=True, title="Within estimator, with lag dependent and het robust")

        beta, fixed_effects, resid_by_n, cov, durbin_watson = within_group(
                data, "S/Y", ["d(lnY)", "INF"], lags=1, title="Within estimator, with lag dependent")


    beta, fixed_effects, resid_by_n, cov, durbin_watson = within_group(
        data, "S/Y", ["d(lnY)", "INF"], cross_sec=True, title="Within estimator, cross sec correction")

    np.save("data/resid.npy", resid_by_n)
