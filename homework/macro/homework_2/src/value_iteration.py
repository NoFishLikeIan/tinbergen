import numpy as np
import numpy.linalg as la

from .fundamentals import make_u


def naive_algorithm(grid, beta, phi, epsilon, verbose=0):
    n = grid.shape[1]

    iteration_count = 0

    current_v = np.zeros(n, )

    instant_utility = make_u(epsilon, phi)

    utility_grid = np.apply_along_axis(
        instant_utility, 0, grid)  # TODO: Slow, can make faster

    distance = []

    if verbose > 0:
        print('Done with utility...')

    for i in range(100):
        if verbose > 0:
            print(f'Iteration: {i+1}/100', end='\r')

        value_grid = utility_grid + np.tile(current_v, (n, 1))
        policy = np.argmax(value_grid, axis=1)
        max_ks = value_grid[np.arange(n), policy]

        d = la.norm(max_ks - current_v)
        distance.append(d)

        current_v[:] = max_ks

    print('\n')
    return current_v, policy, distance
