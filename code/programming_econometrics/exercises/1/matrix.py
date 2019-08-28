import numpy as np
import pandas as pd


def check_matrices(matrix, vector):
    (n, m) = matrix.shape

    if n != m:
        raise ValueError('Matrix is not square')

    (i,) = vector.shape

    if n != i:
        raise ValueError('Non compatible shapes between vector and matrix')


def backsubstitution(matrix, vector):
    check_matrices(matrix, vector)

    result_vector = np.zeros(vector.shape)
    n = result_vector.shape[0] - 1
    result_vector[n] = vector[n] / matrix[n, n]

    for i in reversed(range(n)):
        m = matrix[i][i+1:]
        v = result_vector[i+1:]
        s = np.sum(m * v)

        result_vector[i] = (vector[i] - s) / matrix[i, i]

    return result_vector


def main():

    a_matrix = np.array([
        [6., -2., 2., 4.],
        [0., -4., 2., 2.],
        [0., 0., 2., -5.],
        [0., 0., 0., -3],
    ])

    b_vector = np.array([16., -6., -9., -3.])

    x_vector = backsubstitution(matrix=a_matrix, vector=b_vector)

    b_hat = x_vector @ np.linalg.inv(a_matrix)
    condition = np.allclose(b_vector, b_hat)

    print(f'The result is{" not" if not condition else ""} correct')

    if (not condition):
        print(f'You gave {b_vector}, and it should be {b_hat}')


if __name__ == '__main__':
    main()
