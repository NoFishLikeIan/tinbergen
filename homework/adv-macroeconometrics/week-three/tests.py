import numpy as np

def panel_dw(resid: np.ndarray, N: int, T: int) -> np.float:
    
    variance = np.sum(np.square(resid))
        
    n_sum = np.empty((T-1, N))
    
    for t in range(1, T):
        n_sum[t-1] = np.square(resid[t] - resid[t-1])
        

    return np.sum(n_sum) / variance