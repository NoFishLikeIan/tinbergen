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

    beta = np.linalg.inv(X_dem.T@X_dem)@(X_dem.T@Y_dem)
    resid = Y - X@beta

    resid_by_n = resid.reshape(T, N, order="F")
    fixed_effects = resid_by_n.mean(axis=0)

    cov_fn = nw_corrected if het_robust else white_var

    cov = cov_fn(X_dem, resid, (N, T))

    tests = {
        test_name: fn(resid_by_n) for (test_name, fn) in tests_fns.items()
    }

    _, pesaran_p_value = tests["Pesaran"]

    if cross_sec and pesaran_p_value < .05:
        # TODO: Not clear how to this. Should one stack t-times or only once?

        # Add dummy for cross-sectionally dependent data

        transform.add_dummy(data, regressors)

        return

    if verbose:
        # Print as a table
        printing.pprint(beta, cov, regressors, tests, **print_kwargs)

    return beta, fixed_effects, resid_by_n, cov, tests


if __name__ == '__main__':
    from utils.ingest import read_data

    data = read_data("data/hw3.xls")

    partial = data.loc[(slice(None), slice("1981-01-01")),
                       ["Australia", "Belgium"]]  # test with few data points

    beta, fixed_effects, resid_by_n, cov, durbin_watson = within_group(
        data, "S/Y", ["d(lnY)", "INF"], lags=0, title="Within estimator")

    beta, fixed_effects, resid_by_n, cov, durbin_watson = within_group(
        data, "S/Y", ["d(lnY)", "INF"], lags=1, title="Within estimator, with lag dependent")

    beta, fixed_effects, resid_by_n, cov, durbin_watson = within_group(
        data, "S/Y", ["d(lnY)", "INF"], lags=1, het_robust=True, title="Within estimator, with lag dependent and het robust")

    beta, fixed_effects, resid_by_n, cov, durbin_watson = within_group(
        data, "S/Y", ["d(lnY)", "INF"], cross_sec=True, title="Within estimator, with lag dependent")

    np.save("data/resid.npy", resid_by_n)
