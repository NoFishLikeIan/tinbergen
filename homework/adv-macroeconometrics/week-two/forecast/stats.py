import numpy as np
import pandas as pd

from typing import Union, NewType, Tuple, List

Data = NewType("Data", Union[pd.DataFrame, np.ndarray])

def df_to_data(df: Data) -> Tuple[np.ndarray, List[str]]:

    if isinstance(df, pd.DataFrame):
        X = df.to_numpy()
        var_names = df.columns.tolist()
    else:
        X = df
        var_names = []

    if X.shape[0] > X.shape[1]:
        # Make the array (N, T)
        X = X.T

    return X, var_names

def sample_covariance(df: Data) -> Tuple[np.ndarray, List[str]]:

    X, var_names = df_to_data(df)

    T = X.shape[1]

    Q = np.identity(T) - 1/T * np.ones((T, T))    
    X_dem = Q@X.T

    cov = (X_dem.T@X_dem) * 1/T

    return cov, var_names
