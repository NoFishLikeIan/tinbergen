import pandas as pd
import numpy as np

from typing import Callable, Dict, NewType

Transformer = NewType('Transformer', Callable[[pd.Series], pd.Series])

def diff(series: pd.Series) -> pd.Series:
    return series.diff(1)

def diff_second(series: pd.Series) -> pd.Series:
    N = len(series)
    X = series.to_numpy()

    X_out = np.empty(len(series))
    X_out[:] = np.nan

    zero_X = X[2:]
    one_X = X[1:N-1]
    two_X = X[:N-2]

    second_diff = zero_X - 2*one_X + two_X

    X_out[2:] = second_diff

    return pd.Series(X_out, index = series.index)

def cond_log(series: pd.Series) -> pd.Series:
    if np.min(series) < 1e-6:
        return pd.Series(np.nan, index=series.index)

    return np.log(series)


cases: Dict[int, Transformer] = {
    1: lambda s: s,
    2: diff,
    3: diff_second,
    4: cond_log,
    5: lambda s: diff(cond_log(s)),
    6: lambda s: diff_second(cond_log(s)),
    7: lambda s: diff(s.pct_change())
}

def standard(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to transform data, loosly based on prepare_missing.m

    Parameters
    ----------
    raw_df : pd.DataFrame
    """

    na_latest = raw_df.iloc[-1].isna().all()

    if na_latest:
        raw_df = raw_df.iloc[:-1]

    dates = pd.DatetimeIndex(raw_df.loc[1:, "sasdate"], freq="MS")
    
    core_data = raw_df.loc[1:, "RPI":].copy().set_index(dates)
    variables = core_data.columns

    codes = raw_df.iloc[0, 1:].astype(int)

    transf_df = pd.DataFrame(columns = variables, index = dates)

    for variable, code in zip(variables, codes):
        
        transf_fn = cases[code]

        raw_series = core_data[variable]
        transf_df[variable] = transf_fn(raw_series)


    return transf_df