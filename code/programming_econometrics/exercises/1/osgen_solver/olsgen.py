import numpy as np
import pandas as pd

import solvers
import utils
import read

np.random.seed(11148705)


def gen_observation(X, beta_vector, sigma):
    return X @ beta_vector + np.random.randn(X.shape[0]) * sigma


def generate_X_matrix(n, k, constant=1):
    constants_vector = np.ones((n, 1)) * constant
    random_matrix = np.random.random(size=(n, k))
    return np.hstack((constants_vector, random_matrix))


def main():
    obs_size, sigma = read.read_opt()
    k = 2
    beta = np.linspace(1, k+1, num=k+1, endpoint=True)

    X = generate_X_matrix(n=obs_size, k=k)

    y = gen_observation(X, beta, sigma)

    beta_hat = solvers.estimate_with_mm(X, y)
    _ = solvers.estimate_with_pf(X, y)

    s = utils.compute_s(X, y, beta_hat)
    t = solvers.compute_t_stat(X=X, y=y, beta_hat=beta_hat)

    print(pd.DataFrame(np.array([beta_hat, s, t]).T,
                       columns=['Beta', 's', 't']))


if __name__ == '__main__':
    main()
