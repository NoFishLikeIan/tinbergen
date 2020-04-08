
from functools import wraps
from scipy import integrate
import numpy as np


def is_inbound(fn):
    @wraps(fn)
    def wrapper(self, *args):
        x = args[0]
        if x < self.L or x > self.H:
            raise ValueError(
                f"Argument out of bounds, requires {self.L} < {x} < {self.H}")

        return fn(self, *args)
    return wrapper


class BoundedParetoDensity:
    def __init__(self, alpha: float = 5, L: float = 1, H: float = np.inf):
        if H < L:
            raise ValueError(
                "The lower bound has to be smaller than the upper bound")

        self.alpha = alpha
        self.L = L
        self.H = H

        self.num_factor = self.alpha * (self.L**self.alpha)
        self.den_factor = 1 - (L/H)**alpha

    @is_inbound
    def pdf(self, x: float):
        scaled = x**(-self.alpha-1)

        return self.num_factor*scaled/self.den_factor

    @is_inbound
    def cdf(self, x: float):
        mass, _ = integrate.quad(lambda x: self.pdf(x), self.L, x)

        return mass

    def integrate(self, factor: float = None):
        fn_modifier = factor if factor is not None else lambda _: 1

        limit = 150 if factor is not None else 50

        mass, _ = integrate.quad(
            lambda x: fn_modifier(x)*self.pdf(x),
            self.L,
            self.H,
            limit=limit
        )

        return mass

    @property
    def E(self):
        return self.integrate(lambda x: x)


if __name__ == '__main__':
    d = BoundedParetoDensity(L=2)

    try:
        d.pdf(1)
    except ValueError as e:
        print(e)
        print("Error caught")

    print(d.cdf(100))
    print(d.cdf(2.2))
    print(d.pdf(2.12))
