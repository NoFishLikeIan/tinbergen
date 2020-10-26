import numpy as np
import pandas as pd

from utils import transform, matrix, printing

# --- Typings

from data_types import EstimationResults
from typing import List


def mean_group(data: pd.DataFrame, dependent: str,
               regressors: List[str] = [],
               lags=0, verbose=1, **print_kwargs):

    if len(regressors) == 0:
        regressors = data.index.get_level_values(0).tolist()

    if lags > 0:

        data, lagged_names = transform.make_multi_lagged(
            data, dependent, lags=lags)

        regressors += lagged_names

    _, N = data.loc[dependent].shape
    K = len(regressors)

    delta_is = np.zeros((N, K))

    for i, country in enumerate(data.columns):
        w_unmeaned = data[country].loc[regressors].unstack().T.to_numpy()
        y_unmeaned = data[country].loc[dependent].to_numpy()

        w = w_unmeaned - np.mean(w_unmeaned, axis=0)
        y = y_unmeaned - np.mean(y_unmeaned, axis=0)
        delta_is[i] = (np.linalg.inv(w.T@w)@w.T@y) / N

    delta = delta_is.mean(axis=0)

    var = np.zeros((K, K))
    factor = 1 / (N*(N-1))

    for delta_i in delta_is:
        delta_dem = (delta_i - delta).reshape(-1, 1)
        var += factor*(delta_dem@delta_dem.T)

    if verbose > 0:
        printing.pprint(delta, var, regressors, **print_kwargs)

    return


if __name__ == '__main__':

    from utils.ingest import read_data

    data = read_data("data/hw3.xls")

    mean_group(data, "S/Y", ["U"], lags=1, title="MG Estimator", verbose=1)
