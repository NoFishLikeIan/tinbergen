import numpy as np
from scipy import signal

from typing import Tuple, List


def local_extrema(vec: np.array) -> Tuple[List[int], List[int]]:
    """
    Takes a 1-d np array and return the indices of the
    local maximum and minimum, including boundary points
    """

    maxInd = signal.argrelextrema(vec, np.greater)[0]
    minInd = signal.argrelextrema(vec, np.less)[0]

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


if __name__ == '__main__':
    vec = np.array([2, 1, 2, 3, 2, 1, 2], dtype=np.float)
    mx, mn = local_extrema(vec)

    vec[mx] = np.inf
    vec[mn] = -np.inf

    print(vec)
