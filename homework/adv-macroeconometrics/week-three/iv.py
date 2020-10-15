import numpy as np
import pandas as pd

from utils import transform, matrix, printing

from cov_est import white_var, nw_corrected
from tests import panel_dw

# --- Typings

from typing import List, NewType, Union

# TODO: Instruments can be passed as a dataframe or as a number of lags of the regressors
Instruments = NewType("Instruments", Union[pd.DataFrame, int])

def lagged_iv(
        data: pd.DataFrame, dependent: str, 
        lagged_iv = 1,
        regressors: List[str] = [], 
        het_robust = False, 
        verbose = 1
    ):

    if len(regressors) == 0:
        regressors = data.index.get_level_values(0).tolist()

    if lagged_iv < 1:
        raise ValueError("Specify a numer")
    
    data, iv_variables = transform.make_multi_lagged(data, regressors, lags=lagged_iv)
        
    # add the lagged dependent to the regression        
    data, lagged_names = transform.make_multi_lagged(data, dependent, lags=1)
    regressors += lagged_names


    Z, _, L = matrix.stack_to_columns(data, iv_variables)

    Y, _, _ = matrix.stack_to_columns(data, dependent)
    W, N, T = matrix.stack_to_columns(data, regressors)
    
    Q = np.kron(np.identity(N), matrix.make_Q(T))
    Q_z = np.kron(np.identity(N), matrix.make_Q(L))
    
    W_dem = Q@W
    Y_dem = Q@Y
    Z_dem = Q_z@Z

    P_Z = Z_dem@np.linalg.inv(Z_dem.T@Z_dem)

    fitted_W = P_Z@Z_dem.T@W_dem

    beta = np.linalg.inv(fitted_W.T@fitted_W)@fitted_W.T@Y_dem
    resid = Y - fitted_W@beta

    resid_by_n = resid.reshape(T, N, order="F")
    
    cov = white_var(fitted_W, resid, (N, T))

    if verbose > 0:
        printing.pprint(beta, cov, regressors, title="IV Estimation")

    return


if __name__ == '__main__':
    from utils.ingest import read_data

    data = read_data("data/hw3.xls")


    regs = ["d(lnY)", "INF"]

    lagged_iv(
        data, "S/Y",
        regressors=regs, lagged_iv= 1
    )