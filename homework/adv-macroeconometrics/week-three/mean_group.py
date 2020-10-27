import numpy as np
import pandas as pd

from utils import transform, matrix, printing

# --- Typings

from data_types import EstimationResults
from typing import List


def mean_group(data: pd.DataFrame, dependent: str,
               regressors: List[str] = [],
               lags=0, verbose=1, **print_kwargs) -> EstimationResults:

    if len(regressors) == 0:
        regressors = data.index.get_level_values(0).tolist()

    if lags > 0:

        data, lagged_names = transform.make_multi_lagged(
            data, dependent, lags=lags)

        regressors += lagged_names

    T, N = data.loc[dependent].shape
    K = len(regressors)

    delta_is = np.zeros((N, K))
    lambda_i = np.zeros(N)

    for i, country in enumerate(data.columns):
        w_unmeaned = data[country].loc[regressors].unstack().T.to_numpy()
        y_unmeaned = data[country].loc[dependent].to_numpy()

        w = w_unmeaned - np.mean(w_unmeaned, axis=0)
        y = y_unmeaned - np.mean(y_unmeaned, axis=0)
        coeff = (np.linalg.inv(w.T@w)@w.T@y) / N

        beta, alpha = coeff

        lambd = alpha / (1-beta)

        delta_is[i] = coeff
        lambda_i[i] = lambd

    delta = delta_is.mean(axis=0)
    long_run_lambda = lambda_i.mean(axis = 0)

    var = np.zeros((K, K))
    factor = 1 / (N*(N-1))

    for delta_i in delta_is:
        delta_dem = (delta_i - delta).reshape(-1, 1)
        var += factor*(delta_dem@delta_dem.T)

    resid_by_k = y - w@delta

    if verbose > 0:
        lambda_key = f"Long run effect {regressors[0]} -> {dependent}"

        printing.pprint(
            delta, var, regressors, 
            {lambda_key: [long_run_lambda, None]},
            **print_kwargs)

    return delta, long_run_lambda, resid_by_k, var


if __name__ == '__main__':

    from utils.ingest import read_data

    data = read_data("data/hw3.xls")

    mean_group(data, "S/Y", ["U"], lags=1, title="MG Estimator", verbose=1)
