import numpy as np
import pandas as pd

from collections import defaultdict
from typing import Mapping, Callable, List, Tuple

from data import generate_data
from time import time
from dict_utils import set_at
import multiprocessing as mp


def estimate(T, N, sigmas, coeff, generate_data, estimators):

    y, X = generate_data(T, N, sigmas, coeff)

    betas_error = []

    for estimator_fn in estimators:
        beta, std_error = estimator_fn(y, X)
        betas_error.append((beta, std_error))

    return betas_error


def monte_carlo_estimation(
        T=0, N=0,
        sigmas={},
        coeff={},
        estimators: Mapping[str, Callable] = {},
        iterations: int = 1000,
        generate_data=generate_data
):

    estimator_args = (T, N, sigmas, coeff, generate_data,
                      list(estimators.values()))

    pool = mp.Pool(5)
    results = pool.starmap(
        estimate, [estimator_args for _ in range(iterations)])
    pool.close()

    summary_stat = {method: defaultdict(lambda: [])
                    for method in estimators.keys()}

    for iteration_result in results:
        for n, method in enumerate(estimators.keys()):

            beta, error = iteration_result[n]

            summary_stat[method]['beta'].append(beta)
            summary_stat[method]['error'].append(error)

    for stat in summary_stat.values():
        stat['std'] = np.std(stat['beta'])
        stat['mean'] = np.mean(stat['beta'])

    return summary_stat


def iterative_monte_carlo(param_space, path: List[str], **mc_kwargs) -> Tuple[pd.DataFrame, pd.DataFrame]:

    if type(path) == str:
        path = [path]

    verbose = mc_kwargs.get('verbose', 0)
    if verbose > 0:
        start = time()

    mean_betas = defaultdict(lambda: [])
    mean_std = defaultdict(lambda: [])

    for n, param in enumerate(param_space):

        if verbose > 0:
            print(
                f'Running {param} in {path[-1]}, {n+1}/{len(param_space)}')

        set_at(mc_kwargs, path, param)

        mc = monte_carlo_estimation(**mc_kwargs)

        for model, result in mc.items():
            mean_betas[model].append(result['mean'])
            mean_std[model].append(result['std'])

    if verbose > 0:
        print('Iterated MC took: ', time() - start, 'seconds!')

    betas = pd.DataFrame(mean_betas, index=param_space)
    standard_dev = pd.DataFrame(mean_std, index=param_space)

    return betas, standard_dev


if __name__ == '__main__':
    from data import generate_data
    from estimators import first_diff, fixed_effects

    sigmas = {
        'alpha': 1,
        'epsilon': 1,
        'xi': 1
    }

    coeff = {
        'rho': 0.5,
        'pi': 1,
        'theta': 0,
        'beta': 1
    }

    def ols(y, X):
        return np.linalg.lstsq(y, X)[0], 0

    models = {
        'first_diff': ols,
    }

    def generate_X(*args_data_gen, **kwargs_data_gen):
        _, X = generate_data(*args_data_gen, **kwargs_data_gen)
        y = X[1:]
        X = X[:-1]

        return y, X

    Ts = [10, 20, 30]

    betas, standard_dev = iterative_monte_carlo(
        Ts, 'T', T=None, N=150, sigmas=sigmas, estimators=models, coeff=coeff, generate_data=generate_X, iterations=100)

    print(betas)
