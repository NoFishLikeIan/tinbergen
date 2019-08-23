import numpy as np
from nptyping import Array

beta = np.array([1, 2, 3])
sigma = .25


X = np.array([1., *(np.random.uniform() for _ in range(2))])


def epsilon() -> float:
    return sigma * np.random.uniform()


def generate_y():
    return beta * X + epsilon()


def compute_fitted_slope(X: Array[float, 3], y: Array[float, 3]):
    X_p = X.transpose()
    breakpoint()
    return ((X_p * X)**-1)*X_p*y


def main():
    ys = list(*[generate_y() for _ in range(20)])
    fitted_beta = compute_fitted_slope(np.array(X), np.array(ys))
    print('Beta', fitted_beta)


if __name__ == '__main__':
    main()
