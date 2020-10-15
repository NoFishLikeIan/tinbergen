import numpy as np
import pandas as pd

from utils import transform, matrix, printing

from cov_est import white_var, nw_corrected
from tests import panel_dw

# --- Typings

from typing import List

def within_group(data: pd.DataFrame, dependent: str, 
        regressors: List[str] = [], lags = 0, het_robust = False,
        verbose = 1, **print_kwargs
    ):
    
    if len(regressors) == 0:
        regressors = data.index.get_level_values(0).tolist()
        
    if lags > 0:
        
        data, lagged_names = transform.make_multi_lagged(data, dependent, lags=lags)

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
    fixed_effects = resid_by_n.mean(axis = 0)

    cov_fn = nw_corrected if het_robust else white_var

    cov = cov_fn(X_dem, resid, (N, T))
    
    durbin_watson = panel_dw(resid_by_n, N, T) 
    
    if verbose:
        # Print as a table
        printing.pprint(beta, cov, regressors, durbin_watson, **print_kwargs)
        
    return beta, fixed_effects, resid_by_n, cov, durbin_watson
    

if __name__ == '__main__':
    from utils.ingest import read_data

    data = read_data("data/hw3.xls")

    # partial = data.loc[(slice(None), slice("1981-01-01")), ["Australia", "Belgium"]] # test with few data points

    regs = ["d(lnY)", "INF"]

    beta, fixed_effects, resid_by_n, cov, durbin_watson = within_group(data, "S/Y", regs, lags = 1, het_robust=False)