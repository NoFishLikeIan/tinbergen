import numpy as np
import pandas as pd

from numpy.linalg import inv

from utils import transform, matrix, printing

from cov_est import white_var, nw_corrected, white_var_2sls
from tests import panel_dw

# --- Typings

from typing import List, NewType, Union, Tuple

# TODO: Instruments can be passed as a dataframe or as a number of lags of the regressors
Instruments = NewType("Instruments", Union[pd.DataFrame, int])

GmmVariables = NewType(
    "GmmVariables", Tuple[np.ndarray, np.ndarray, np.ndarray, int, int]
)


def extract_regs(data: pd.DataFrame, dependent: str, regressors: List[str], lag_instruments: int) -> GmmVariables:
    """
    Constructs the de-meaned Z, W, Y matrices. Returns the three matrices and the original size N, T
    """
    data, instruments = transform.make_multi_lagged(
        data, regressors, lags=lag_instruments)

    # add the lagged dependent to the regression
    data, lagged_names = transform.make_multi_lagged(data, dependent, lags=1)
    regressors += lagged_names

    Z_unmean, _, _ = matrix.stack_to_columns(data, instruments)

    Y_unmean, _, _ = matrix.stack_to_columns(data, dependent)
    W_unmean, N, T = matrix.stack_to_columns(data, regressors)

    Q = np.kron(np.identity(N), matrix.make_Q(T))

    W = Q@W_unmean
    Y = Q@Y_unmean
    Z = Q@Z_unmean

    return Z, W, Y, N, T


def lagged_gmm(
    data: pd.DataFrame, dependent: str,
    lag_inst=1,
    regressors: List[str] = [],
    het_robust=False, iv=False,
    verbose=1
):

    if len(regressors) == 0:
        regressors = data.index.get_level_values(0).tolist()

    if lag_inst < 1:
        raise ValueError("Specify a number for lag_inst")

    Z, W, Y, N, T = extract_regs(data, dependent, regressors, lag_inst)

    if iv:
        Pi = Z.T@Z
    else:
        Pi = np.identity

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

    lagged_gmm(
        data, "S/Y",
        regressors=regs, lag_inst=1
    )
