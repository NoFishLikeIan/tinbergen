import numpy as np
import scipy.optimize as opt

from matrices import Diff_matrix
from estimators import arellano_bond


def standard_gmm(y, X):
    Z = make_instrument(X, 'standard')

    return estimate(y, X, Z)


def diagonal_gmm(y, X):
    Z = make_instrument(X, 'diagonal')
    return estimate(y, X, Z)


def lagged_gmm(y, X):
    Z = make_instrument(X, 'lagged')
    return estimate(y, X, Z)


def estimate(y, X, Z):

    N, T = X.shape
    D = Diff_matrix(T)

    y_diff = (y @ D.T)
    X_diff = (X @ D.T)

    w_i = np.array([Z[i].T @ D @ D.T @ Z[i] for i in range(N)])

    inv_W = np.sum(w_i, axis=0)

    if isinstance(inv_W, np.float):
        inv_W = inv_W.reshape(1, 1)

    W_n = np.linalg.inv(inv_W)

    beta = arellano_bond(y_diff, X_diff, Z, W_n)

    std_error = np.linalg.norm(y_diff.reshape(-1, 1) -
                               beta*X_diff.reshape(-1, 1).T)/N

    return np.asscalar(beta), std_error


def make_instrument(X, case):
    N, T = X.shape
    Z_standard = X[:, :-1]

    if case == 'standard':
        return Z_standard

    elif case == 'diagonal':
        Z_diag = np.array([np.diag(Z_standard[i])
                           for i in range(Z_standard.shape[0])])

        return Z_diag

    elif case == 'lagged':
        T_h = int(0.5*(T-1)*(T-2) + (T-1))
        Z_lagged = np.zeros((N, T-1, T_h))

        for i in range(N):
            for t in range(T-1):
                row = np.zeros(T_h)
                instrument_x = X[i, :t+1]
                ext = int(0.5*(t + 1)*t)
                row[ext: ext+len(instrument_x)] = instrument_x

                Z_lagged[i][t] = row

        return Z_lagged

    else:
        raise ValueError('No correct case inserted!')


if __name__ == '__main__':
    from data import generate_data
    from estimators import first_diff

    sigmas = {
        'alpha': 1,
        'epsilon': 1,
        'xi': 1
    }

    coeff = {
        'rho': 0.99,
        'pi': 1,
        'theta': 0,
        'beta': 1
    }

    N = 100
    T = 5

    _, X = generate_data(T, N, sigmas, coeff)
    X = X.reshape(-1, 1)
    X_curr = X[1:]
    X_prev = X[:-1]

    print(standard_gmm(X_curr, X_prev))
