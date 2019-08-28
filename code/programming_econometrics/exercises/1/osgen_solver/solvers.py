import numpy as np
import utils


@utils.check_shape_inputs
def estimate_with_mm(X, y):

    beta_hat = np.linalg.inv(X.T @ X) @ X.T @ y

    return beta_hat


@utils.check_shape_inputs
def estimate_with_pf(X, y):
    beta_hat, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

    return beta_hat


def compute_t_stat(X, y, beta_hat):
    return beta_hat / utils.compute_s(X, y, beta_hat)
