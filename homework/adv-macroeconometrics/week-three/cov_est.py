import numpy as np

def white_var(X: np.ndarray, e: np.ndarray) -> np.ndarray:
    inverse = np.linalg.inv(X.T@X)
    
    # construct diagonal array
    diag = np.diag(np.diag(e@e.T))
    
    var_matrix = X.T@diag@X
    
    return inverse@var_matrix@inverse