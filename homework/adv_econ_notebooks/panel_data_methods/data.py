from typing import Mapping, Callable
import numpy as np


def stationary_x(alpha: np.array, rho: float, pi: float, theta: float, **_) -> np.array:
    N, _ = alpha.shape
    den = 1-rho
    den_squared = np.sqrt(den * (1+rho))
    v = np.random.normal(0, 1, (N, 1))
    xi = np.random.normal(0, 1, (N, 1))

    alpha_init = (pi*alpha[:, 0]) / den
    disturbance_init = (theta*v + xi) / den_squared

    return alpha_init + disturbance_init[:, 0]


def generate_data(
    T: int,
    N: int,
    sigmas: Mapping[str, float],
    coeff: Mapping[str, float]
) -> np.array:

    alpha_unstacked = np.random.normal(0, sigmas['alpha'], (N, 1))
    alpha = alpha_unstacked @ np.ones((1, T))

    epsilon = np.random.normal(0, sigmas['epsilon'], (N, T))

    init_x = stationary_x(alpha, **coeff)

    X = np.zeros((N, T))

    xi = np.random.normal(0, sigmas['xi'], (N, T))

    for t in range(T):
        prev_X = X[:, t-1] if t > 0 else init_x
        X[:, t] = coeff['rho'] * prev_X + coeff['pi'] * \
            alpha[:, 0] + coeff['theta'] * epsilon[:, t-1]

    X = X + xi

    y = coeff['beta'] * X + alpha + epsilon

    return y, X
