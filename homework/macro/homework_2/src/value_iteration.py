import numpy as np
import numpy.linalg as la
from scipy.spatial.distance import euclidean


def naive_algorithm(utility_grid, beta, phi, epsilon, verbose=0):
    n = utility_grid.shape[1]

    iteration_count = 0

    current_v = np.zeros(n, )

    distance = []

    if verbose > 0:
        print('Done with utility...')

    for i in range(10):
        value_grid = utility_grid + np.tile(current_v, (n, 1))
        breakpoint()
        policy = np.argmax(value_grid, axis=1)
        max_ks = value_grid[np.arange(n), policy]
        d = euclidean(max_ks, current_v)
        distance.append(d)

        current_v[:] = max_ks

        if verbose > 0:
            print(f'Iteration: {i+1}/100 \n Distance: {d}')

    print('\n')
    return current_v, policy, distance
