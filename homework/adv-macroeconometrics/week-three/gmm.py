import numpy as np
import pandas as pd

from numpy.linalg import inv

from utils import transform, matrix, printing, instruments

from statistics.cov_est import white_var, nw_corrected, white_var_2sls
from statistics.tests import panel_dw, overident_restr, hausman_test

# --- Typings

from typing import List, NewType, Union, Tuple
from data_types import EstimationResults

# TODO: Instruments can be passed as a dataframe or as a number of lags of the regressors
Instruments = NewType("Instruments", Union[pd.DataFrame, int])


def lagged_gmm(
        data: pd.DataFrame, dependent: str,
        lag_inst=1,
        regressors: List[str] = [],
        het_robust=False, gmm=False,
        is_lagged_instrumented=False,
        verbose=1, **print_kwargs) -> EstimationResults:

    tests = {}

    if len(regressors) == 0:
        regressors = data.index.get_level_values(0).tolist()

    if lag_inst < 1:
        raise ValueError("Specify a number for lag_inst")

    Z, W, Y, N, T = instruments.extract_regs(
        data,
        dependent,
        regressors,
        lag_inst,
        is_lagged_instrumented,
        verbose
    )

    L, K = Z.shape[1], W.shape[1]

    if L < K:
        raise ValueError("System is underidentified")

    W_f = Z@inv(Z.T@Z)@Z.T@W

    beta = inv(W_f.T@W_f)@W_f.T@Y

    resid = Y - W@beta
    
    cov, S_hat = white_var_2sls(W, Z, resid)

    if het_robust:
        cov = nw_corrected(W, resid, (N, T))

    if gmm:
        L = Z.shape[1]
        K = W.shape[1]

        # --- Generalize the IV for Hansen, 1982

        inv_S = inv(S_hat)
        beta = inv(W.T@Z@inv_S@Z.T@W)@(W.T@Z@inv_S@Z.T)@Y

        resid = Y - W@beta

        cov = (N*T)*inv(W.T@Z@inv_S@Z.T@W)

        # --- OIR Test

        stat, p_value = overident_restr(Z, resid, inv_S, L, K)
        tests["Overidentifying Restrictions"] = [stat, p_value]

        # --- Hausman test

        within_beta = inv(W.T@W)@W.T@Y
        within_e = Y - W@within_beta
        within_var = white_var(W, within_e)

        stat, p_value = hausman_test(within_beta, beta, within_var, cov)
        tests["Hausman"] = [stat, p_value]


    resid_by_n = resid.reshape(T, N, order="F")
    durbin_watson = panel_dw(resid_by_n)

    tests["Durbin-Watson"] = durbin_watson

    if verbose > 0:
        
        estimator = "GMM" if gmm else "IV"
        def_title = f"{estimator} estimation of ({', '.join(regressors)}) -> {dependent} "

        title = print_kwargs.get("title", def_title)

        printing.pprint(beta, cov, regressors, tests, title=title)

    return beta, resid_by_n, cov, durbin_watson


if __name__ == '__main__':
    from utils.ingest import read_data

    data = read_data("data/hw3.xls")


    lags = 2

    if False:

        lagged_gmm(
            data, "S/Y",
            regressors=["d(lnY)", "INF"], lag_inst=lags, is_lagged_instrumented=True, 
        )


        lagged_gmm(
            data, "S/Y",
            regressors=["d(lnY)", "INF"], lag_inst=lags, is_lagged_instrumented=True, 
            gmm=True
        )

        _, _, cov, _ = lagged_gmm(
            data, "S/Y",
            regressors=["d(lnY)", "INF"], lag_inst=lags, is_lagged_instrumented=True, 
            het_robust=True
        )

        with open("data/cov.tex", "w") as file:
            file.write(printing.np_to_pmatrix(np.diag(cov).reshape(-1, 1), prec=6))
        

    if True:

        beta, _, cov, _ = lagged_gmm(
            data, "S/Y",
            regressors=["SG/Y"], lag_inst=lags, 
            is_lagged_instrumented=True
        )

        printing.save_as(beta, "q5-IV-beta")
        printing.save_as(np.sqrt(np.diag(cov)).reshape(-1, 1), "q5-IV-cov")


        beta, _, cov, _ = lagged_gmm(
            data, "S/Y",
            regressors=["SG/Y"], lag_inst=lags, 
            gmm=True,
            is_lagged_instrumented=True
        )

        printing.save_as(beta, "q5-gmm-beta")
        printing.save_as(np.sqrt(np.diag(cov)).reshape(-1, 1), "q5-gmm-cov")

