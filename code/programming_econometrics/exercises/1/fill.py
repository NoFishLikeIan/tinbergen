import numpy as np


def mutate_prod_index_matrix(matrix):
    for (r, c), _ in np.ndenumerate(matrix):
        matrix[r][c] = r * c

    return matrix


def generate_prod_index_matrix(i, k):
    x = np.zeros((i, k))
    mutate_prod_index_matrix(x)

    return x


def one_line_fill(i, k):
    return np.array([[row * col for row in range(i)] for col in range(k)])


def main():
    xM = one_line_fill(10, 10)
    print(xM)


if __name__ == '__main__':
    main()
