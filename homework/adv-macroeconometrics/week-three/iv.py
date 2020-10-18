import numpy as np
import pandas as pd

from numpy.linalg import inv

from utils import transform, matrix, printing

from cov_est import white_var, nw_corrected, white_var_2sls
from tests import panel_dw

# --- Typings

from typing import List, NewType, Union

# TODO: Instruments can be passed as a dataframe or as a number of lags of the regressors
Instruments = NewType("Instruments", Union[pd.DataFrame, int])


def lagged_iv(
    data: pd.DataFrame, dependent: str,
    lagged_iv=1,
    regressors: List[str] = [],
    het_robust=False,
    verbose=1
):

    if len(regressors) == 0:
        regressors = data.index.get_level_values(0).tolist()

    if lagged_iv < 1:
        raise ValueError("Specify a numer")

    data, iv_variables = transform.make_multi_lagged(
        data, regressors, lags=lagged_iv)

    # add the lagged dependent to the regression
    data, lagged_names = transform.make_multi_lagged(data, dependent, lags=1)
    regressors += lagged_names

    Z_unmean, _, L = matrix.stack_to_columns(data, iv_variables)

    Y_unmean, _, _ = matrix.stack_to_columns(data, dependent)
    W_unmean, N, T = matrix.stack_to_columns(data, regressors)

    Q = np.kron(np.identity(N), matrix.make_Q(T))

    W = Q@W_unmean
    Y = Q@Y_unmean
    Z = Q@Z_unmean

    W_f = Z@inv(Z.T@Z)@Z.T@W

    beta = inv(W_f.T@W_f)@W_f.T@Y

    resid = Y - W@beta

    cov = white_var_2sls(W, W_f, resid)

    resid_by_n = resid.reshape(T, N, order="F")

    durbin_watson = panel_dw(resid_by_n, N, T)

    if verbose > 0:
        printing.pprint(beta, cov, regressors,
                        durbin_watson, title="IV Estimation")

    return beta, resid_by_n, cov, durbin_watson


if __name__ == '__main__':
    from utils.ingest import read_data

    data = read_data("data/hw3.xls")

    regs = ["d(lnY)", "INF"]

    lagged_iv(
        data, "S/Y",
        regressors=regs, lagged_iv=1
    )
