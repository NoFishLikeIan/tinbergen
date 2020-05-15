import numpy as np
from scipy import signal

from typing import Tuple, List


def local_extrema(vec: np.array) -> Tuple[List[int], List[int]]:
    """
    Takes a 1-d np array and return the indices of the
    local maximum and minimum, including boundary points
    """

    maxInd = signal.argrelmax(vec)[0]
    minInd = signal.argrelmin(vec)[0]

    # TODO: Find a better way to do this because "argrelextrema" only looks for internal
    if vec[0] > vec[1]:
        maxInd = np.append(maxInd, 0)
    else:
        minInd = np.append(minInd, 0)

    if vec[-1] > vec[-2]:
        maxInd = np.append(maxInd, len(vec) - 1)
    else:
        minInd = np.append(minInd, len(vec) - 1)

    return maxInd, minInd


def stability_equil(vec: np.array,
                    equil: np.float = 1.,
                    extreme=True,
                    atol=1e-3
                    ) -> Tuple[np.array, np.array]:
    """
    Finds gradient of intersaction with equil axes of 1d array.
    Returns index of intersection and gradient.

    If extreme, it includes boundary point in the equilibrium.
    """
    equil_vec = equil*np.ones(vec.shape)

    equil_points = np.where(np.isclose(vec, equil_vec, atol=atol))[0]

    if extreme:
        # TODO: Find more numpy way to do this
        equil_points = np.concatenate([[0], equil_points, [len(vec)-1]])

    equil_points = np.unique(equil_points)
    gradients = np.gradient(vec[equil_points])

    return equil_points, gradients


if __name__ == '__main__':
    vec = np.array([2, 1, 2, 3, 2, 1, 0], dtype=np.float)
    print(stability_equil(vec))
