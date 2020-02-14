import numpy as np
from matrices import Q_matrix, Diff_matrix


def pooled(y, X):
    N, T = X.shape

    intercept = np.kron(np.identity(N), np.ones((T, 1)))

    W = np.concatenate((intercept, X.reshape(-1, 1)), axis=1)
    y_stacked = y.reshape(-1, 1)

    theta_hat, e, *_ = np.linalg.lstsq(W, y_stacked, rcond=None)
    std_error = e/N

    return theta_hat[-1, 0], std_error


def fixed_effects(y, X):
    N, T = X.shape

    Q = Q_matrix(T)
    X_dem = (X @ Q).reshape(-1, 1)
    y_dem = (y @ Q).reshape(-1, 1)
    beta_hat, e, *_ = np.linalg.lstsq(X_dem, y_dem, rcond=None)

    std_error = e/N

    return beta_hat[-1, 0], std_error[0]


def first_diff(y, X):
    N, T = X.shape

    D = Diff_matrix(T)
    X_diff = (X @ D.T).reshape(-1, 1)
    y_diff = (y @ D.T).reshape(-1, 1)

    beta_hat, e, *_ = np.linalg.lstsq(X_diff, y_diff, rcond=None)

    std_error = e/N

    return beta_hat[-1, 0], std_error[0]


def arellano_bond(y, X, Z, W_n=None):
    W_n = W_n if W_n is not None else np.identity(Z.shape[1])

    X_Z = np.sum([X[i].T @ Z[i]
                  for i in range(X.shape[0])], axis=0, keepdims=True)
    Z_X = np.sum([Z[i].T @ X[i]
                  for i in range(X.shape[0])], axis=0, keepdims=True)

    Z_y = np.sum([Z[i].T @ y[i]
                  for i in range(y.shape[0])], axis=0, keepdims=True)

    den_variance = X_Z@W_n@Z_X.T

    if isinstance(den_variance, np.float):
        den_variance = den_variance.reshape(1, 1)

    inv = np.linalg.inv(den_variance)

    beta = inv @ X_Z @ W_n @Z_y.T

    return beta
