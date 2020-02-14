import numpy as np


def Diff_matrix(T):
    return -1*np.eye(T-1, T) + np.eye(T-1, T, k=1)


def Q_matrix(T):
    return np.identity(T) - np.ones((T, T))/T


def projection(X):
    return X @ np.linalg.inv(X.T @ X) @ X.T


def residual_matrix(X):

    P = projection(X)
    return np.identity(P.shape[0]) - P
