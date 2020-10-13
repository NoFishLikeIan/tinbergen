import numpy as np
import pandas as pd

from typing import List, NewType, Tuple

StackingResult = Tuple[np.ndarray, int, int]

def stack_to_columns(data: pd.DataFrame, variables: List[str]) -> StackingResult:
    """
    Takes the panel data and returns an array of size,
    NT x len(cols)
    """
    
    if isinstance(variables, str):
        variables = [variables]
    
    # Assumes that the panel has fixed size
    T, N = data.loc[data.index[0][0]].shape
    n_variables = len(variables)
    
    X = np.empty((N*T, n_variables))
        
    for i, var in enumerate(variables):
        
        # requires transposition for N->T stacking and not T->N stacking 
        var_df = data.loc[var].T
        
        X[:, i] = var_df.to_numpy().reshape(-1, )

    return X, N, T
    

def make_Q(T: int) -> np.ndarray:
    """
    Make a de-meaning matrix
    """
    iota = np.ones((T, 1))
    
    return np.identity(T) - iota@iota.T/T