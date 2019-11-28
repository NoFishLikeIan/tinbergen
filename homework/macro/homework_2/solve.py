import numpy as np

from src import value_iteration
from src.grid_setup import make_grid
from src.fundamentals import make_u

alpha = 0.1
k_extent = [1e-3, 1]
n = 5
beta = 0.001
phi = 30
epsilon = 0.001
cache_dir = 'cache/utility.npy'
cache = False

if __name__ == '__main__':
    import seaborn as sns
    import time
    import os

    if os.path.isfile(cache_dir) and cache:
        print('Reading grid from cache...')
        utility_grid = np.load(cache_dir)

    else:
        print('Making grid...')
        grid = make_grid(n, k_extent, alpha)
        instant_utility = make_u(epsilon, phi)

        utility_grid = np.apply_along_axis(
            instant_utility, 0, grid).T  # TODO: Slow, can make faster

        np.save(cache_dir, utility_grid)

    print('Done! Optimizing...')

    v, policy, distances = value_iteration.naive_algorithm(
        utility_grid, beta, phi, epsilon, verbose=1)

    print('Done!')

    ax = sns.lineplot(x=range(len(distances)), y=distances)
    fig = ax.get_figure()
    fig.savefig(f'out/distances_{int(time.time())}.png')
