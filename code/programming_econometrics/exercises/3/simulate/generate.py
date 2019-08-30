import numpy as np


def gen_ys(X, beta, sigma, l, cached=False):
    """
    Generate simulated ys, or fetch if cached

    Parameters
    ----------
    X : Matrix[k, n]
    beta : Vector[n]
    sigma : number
    l : number

    Returns
    -------
    y
        Vector[n]
    """
    (n, _) = X.shape
    y = X @ beta + np.random.randn(n) * sigma * l
    return y
