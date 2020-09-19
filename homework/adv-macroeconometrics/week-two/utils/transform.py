import pandas as pd
import numpy as np

from typing import Callable, Dict, NewType

Transformer = NewType('Transformer', Callable[[pd.Series], pd.Series])


def diff(order: int) -> Transformer:
    def apply(series: pd.Series) -> pd.Series:
        return series.diff(order)

    return apply

def cond_log(series: pd.Series) -> pd.Series:
    if np.min(series) < 1e-6:
        return pd.Series(np.nan, index=series.index)

    return np.log(series)


cases: Dict[int, Transformer] = {
    1: lambda s: s,
    2: diff(1),
    3: diff(2),
    4: cond_log,
    5: lambda s: diff(1)(cond_log(s)),
    6: lambda s: diff(2)(cond_log(s)),
    7: lambda s: diff(1)(s.pct_change())
}

def transform_data(raw_df: pd.DataFrame):
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