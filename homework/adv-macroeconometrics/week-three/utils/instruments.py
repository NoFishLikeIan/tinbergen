import numpy as np
import pandas as pd

from .matrix import stack_to_columns, make_Q
from .transform import make_multi_lagged

from typing import NewType, Tuple, List

GmmVariables = NewType(
    "GmmVariables", Tuple[np.ndarray, np.ndarray, np.ndarray, int, int]
)


def extract_regs(
        data: pd.DataFrame,
        dependent: str,
        regressors: List[str],
        lag_instruments: int,
        is_lagged_instrumented=False,
        verbose=0) -> GmmVariables:
    """
    Constructs the de-meaned Z, W, Y matrices. Returns the three matrices and the original size N, T
    """

    if is_lagged_instrumented:
        # Note that the order here is swapped so that instruments are generated for y(t - 1)
        # add the lagged dependent to the regression
        data, lagged_names = make_multi_lagged(data, dependent, lags=1)
        regressors += lagged_names

        data, instruments = make_multi_lagged(
            data, regressors, lags=lag_instruments)

    else:
        data, instruments = make_multi_lagged(
            data, regressors, lags=lag_instruments)

        data, lagged_names = make_multi_lagged(data, dependent, lags=1)
        regressors += lagged_names

    Z_unmean, _, _ = stack_to_columns(data, instruments)

    Y_unmean, _, _ = stack_to_columns(data, dependent)
    W_unmean, N, T = stack_to_columns(data, regressors)

    Q = np.kron(np.identity(N), make_Q(T))

    W = Q@W_unmean
    Y = Q@Y_unmean
    Z = Q@Z_unmean

    return Z, W, Y, N, T
