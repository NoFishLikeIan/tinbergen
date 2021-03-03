import pandas as pd
import numpy as np

from typing import List


def make_lagged_data(data: pd.DataFrame, variable: str, var_name=None) -> pd.DataFrame:

    if var_name is None:
        var_name = f"lag_1_{variable}"

    days = data.index.get_level_values("date")
    first_day = days[0]
    second_day = days[1]

    lagged_data = data.loc[variable].iloc[:-1].to_numpy()

    lagged_df = data.loc[variable].copy()
    lagged_df.loc[second_day:] = lagged_data

    lagged_df.index = pd.MultiIndex.from_product(
        [[f"{var_name}"], lagged_df.index], names=['variable', 'date'])

    data_with_lag = data.append(lagged_df)
    data_with_lag = data_with_lag.drop(first_day, level="date")

    return data_with_lag


def make_multi_lagged(data: pd.DataFrame, variables: List[str], lags=1) -> pd.DataFrame:

    lagged_var_names = []

    if isinstance(variables, str):
        variables = [variables]

    for null_var in variables:
        variable_to_lag = null_var

        for l in range(lags):
            var_name = f"lag_{l+1}_{null_var}"
            data = make_lagged_data(data, variable_to_lag, var_name=var_name)

            variable_to_lag = var_name

            lagged_var_names.append(var_name)

    return data, lagged_var_names


def make_dummy(data: pd.DataFrame, variables: List[str], N: int, T: int) -> pd.DataFrame:
    """
    Add data for dummy regression. This is implemented adding 
    the mean of the regression variable.
    """

    K = len(variables)
    dummy_matrix = np.zeros((N*T, K))

    for i, var in enumerate(variables):
        cs_mean = data.loc[var].mean()
        
        dummy_matrix[:, i] = np.repeat(cs_mean, T)


    return dummy_matrix
