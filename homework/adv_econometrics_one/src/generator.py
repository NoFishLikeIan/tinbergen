import numpy as np
import json

from scipy import stats
from collections import defaultdict
from itertools import product

np.random.seed(11148705)


def nested_dict():
    return defaultdict(nested_dict)


def n_data_gen(n):
    return np.random.normal(size=int(n))


def t_data_gen(n):
    return stats.nct.rvs(2, 0, size=int(n))


def sample_std(arr, r=1000):
    s = np.sum(np.square(arr))

    return np.sqrt(s) / r


normal_density = stats.norm.pdf(0, 0, 1)
t_density = stats.nct.pdf(0, 2, 0, 0, 1)


generators = [('normal', n_data_gen), ('t-student', t_data_gen)]
statistics = [('mean', np.mean), ('median', np.median)]
tests = [('standard_deviation', sample_std),
         ('jarque_bera', lambda arr: stats.jarque_bera(arr)[1])]


def asymptotic_std_median(sample, densities=[normal_density, t_density]):

    return (
        np.sqrt(1 / (4*sample*density)) for density in densities
    )


def gen_mean_median_data(
    samples=[10, 25, 100, 500, 1000],
    replications=1000,
    generators=generators,
    statistics=statistics,
    tests=tests,
    save=False
):

    report = nested_dict()
    sampled_data = {}

    for n, g in product(samples, generators):
        distr, generate_sample = g

        for statistic_name, compute_stat in statistics:
            data = (generate_sample(n) for _ in range(replications))
            samples_statistic = [compute_stat(sample) for sample in data]
            flat_key = f'{n}_{distr}_{statistic_name}'
            sampled_data[flat_key] = samples_statistic

            for test_name, run_tests in tests:
                report[flat_key][test_name] = run_tests(samples_statistic)

    if save:

        with open('statistics.json', 'w') as file:
            json.dump(report, file)

        print('File saved!')

    return report, sampled_data
