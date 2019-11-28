import numpy as np
import os

from .fundamentals import max_prod_function


def g_mapper(alpha):
    def map_to_g(coords):
        k, k_prime = coords
        attainable_k = max_prod_function(k, alpha)

        if k_prime > attainable_k:
            return np.array([k, -np.inf])
        else:
            return coords

    return map_to_g


def make_grid(n, k, alpha):

    low, high = k
    k_axis = np.linspace(start=low, stop=high, num=n)
    axis = np.meshgrid(k_axis)

    unfeasable_grid = np.array(np.meshgrid(k_axis, k_axis))

    grid = np.apply_along_axis(g_mapper(alpha), 0, unfeasable_grid)

    return grid
