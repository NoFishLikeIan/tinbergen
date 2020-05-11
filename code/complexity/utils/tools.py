from functools import reduce


def fn_dot(f, g):
    return lambda *a: f(g(*a))


def fn_iterate(f, n: int):
    return reduce(fn_dot, (f for _ in range(n)))
