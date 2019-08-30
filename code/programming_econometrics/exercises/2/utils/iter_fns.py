import numpy as np
from itertools import product


def compute_percentage_difference(iterable):
    return [100*(np.log(n_1) - np.log(n_0)) for n_1, n_0 in zip(iterable[1:], iterable)]


def map_product(fn, *iterables):
    '''
    Maps a function to the product of iterables and unzips
    '''
    return zip(*(fn(*items) for items in product((*iterables))))
