from collections.abc import Iterable


def sequential_squared_loss(fns, expected, args=[]):
    """
    Compute square loss of functions array with common arguments
    """

    if not isinstance(fns, Iterable):
        fns = [fns]

    if not isinstance(expected, Iterable):
        expected = [expected]

    if len(fns) != len(expected):
        raise ValueError('Number of functions and constraints does not match')

    aggregate_squared_loss = 0

    for function, expected_value in zip(fns, expected):
        loss = function(*args) - expected_value

        squared_loss = loss * loss
        aggregate_squared_loss += squared_loss

    return aggregate_squared_loss


def squared_loss(function, expected_value, args):
    loss = function(*args) - expected_value

    squared_loss = loss * loss
    return squared_loss


if __name__ == '__main__':
    def ret_1(): return 1

    loss = sequential_squared_loss(ret_1, 1)

    assert loss == 0, f"Loss function not working, expected 0, got {loss}"

    def ret_2(): return 2

    loss = sequential_squared_loss([ret_2, ret_2], [0, 4])

    assert loss == 8, f"Loss function not working, expected 4, got {loss}"
