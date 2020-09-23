import numpy as np
import pandas as pd

from statsmodels.tsa import stattools

from typing import Union, NewType, Tuple, List, Dict, Callable

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

def acf(df: Data) -> Dict[str, np.ndarray]:

    X, var_names = df_to_data(df)

    acfs = {}

    for i, series in enumerate(X):
        acf, conf = stattools.acf(series, nlags=15, fft=True, alpha=.05)
        acf_mat = np.concatenate((acf.reshape(-1, 1), conf), axis = 1)

        acfs[var_names[i]] = acf_mat

    return acfs

def spectral_density(X: pd.Series, l: float = None) -> Callable[[float], float]:
    """
    Function that estimates the spectral density based on Bartlett kernel

    Parameters
    ----------
    X : pd.Series
    l : float, optional, by default None

    Returns
    -------
    Callable[[float], float]
    """
    
    N = len(X)
    hs = np.arange(1-N, N-1)

    density_space = np.linspace(0, 2*np.pi, num=N)

    acf = stattools.acf(X, fft=True, nlags = N)

    l = min(l, N) if l is not None else N

    @np.vectorize
    def gamma(h):
        return acf[np.abs(h)]

    @np.vectorize
    def w_bar_filter(h):
        if np.abs(h) > l: 
            return 0

        return 1 - np.abs(h)/(l + 1)

    weights = w_bar_filter(hs)
    we_gamma = weights*gamma(hs)

    @np.vectorize
    def apply_to_dens(freq: float):

        cosines = np.cos(freq*hs)
        f_hat = np.sum(we_gamma*cosines)

        dens = f_hat / (2 * np.pi)


        return dens

    densities = apply_to_dens(density_space)

    return densities
