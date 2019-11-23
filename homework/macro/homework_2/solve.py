import numpy as np

from src import value_iteration
from src.grid_setup import make_grid

alpha = 0.1
k_extent = [1e-3, 1]
n = 1000
beta = 0.01
phi = 30
epsilon = 1

if __name__ == '__main__':
    import seaborn as sns
    import time

    print('Making grid...')

    grid = make_grid(n, k_extent, alpha)

    print('Done! Optimizing...')

    v, policy, distances = value_iteration.naive_algorithm(
        grid, beta, phi, epsilon, verbose=1)

    print('Done!')

    ax = sns.lineplot(x=range(len(distances)), y=distances)
    fig = ax.get_figure()
    fig.savefig(f'out/distances_{int(time.time())}.png')
