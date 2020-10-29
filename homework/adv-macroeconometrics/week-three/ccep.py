import numpy as np
import pandas as pd

from utils import transform, matrix, printing

from statistics.cov_est import white_var, nw_corrected
from statistics.tests import panel_dw, pesaran_cd, TestResult

from utils.residual_transformation import cross_correlation
from utils.matrix import make_projection

# --- Typings

from data_types import EstimationResults
from typing import List


def make_M(data: pd.DataFrame, dependent: str, regressors: List[str], N: int, T: int):

    # Gets a matrix of T x Regressors
    means = data.loc[[dependent, *regressors]].mean(axis=1).unstack(level=0)

    means["const"] = 1

    m = means[["const", dependent, *regressors]].to_numpy()

    M = np.kron(np.identity(N), m)

    return M


def ccep(data: pd.DataFrame, dependent: str,
         regressors: List[str] = [],
         lags = 1, 
         verbose=1, **print_kwargs):

    if len(regressors) == 0:
        regressors = data.index.get_level_values(0).tolist()

    if lags > 0:
        data, lagged_names = transform.make_multi_lagged(data, dependent, lags=lags)

        regressors += lagged_names

    # stack the Y variable
    Y, _, _ = matrix.stack_to_columns(data, dependent)
    W, N, T = matrix.stack_to_columns(data, regressors)

    M = make_M(data, dependent, regressors, N, T)

    P = make_projection(M)

    beta = np.linalg.inv(W.T@P@W)@W.T@P@Y

    e = Y - P@W@beta

    resid_by_n = e.reshape(T, N, order="F")

    cov = white_var(P@W, e)

    if verbose:
        # Print as a table
        printing.pprint(beta, cov, regressors, **print_kwargs)

    return beta, resid_by_n, cov


if __name__ == '__main__':
    from utils.ingest import read_data

    data = read_data("data/hw3.xls")

    beta, resid_by_n, cov = ccep(
        data, "S/Y",
        ["d(lnY)", "INF"],  
        lags = 1,
        title="CCEP estimator"
    )

    with open("data/ccep_beta.tex", "w") as file:
        file.write(printing.np_to_pmatrix(beta, prec=5))

    
    with open("data/ccep_cov.tex", "w") as file:
        file.write(printing.np_to_pmatrix(
            np.diag(np.sqrt(cov)).reshape(-1, 1), prec=5
        ))

