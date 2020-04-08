
from scipy import integrate
import numpy as np


class BoundedParetoDensity:
    def __init__(self, alpha: float = 5, L: float = None, H: float = None):
        one_none = H is None or L is None

        if not one_none and H < L:
            raise ValueError(
                "The lower bound has to be smaller than the upper bound")

        den_scaler = (L/H)**alpha if H is not None else 0

        self.alpha = alpha
        self.L = -np.inf if L is None else L
        self.H = np.inf if H is None else H

        self.num_factor = self.alpha * (self.L**self.alpha)
        self.den_factor = 1 - den_scaler

    def is_inbound(self, x: float):
        if self.L is not None and x < self.L:
            return False

        if self.H is not None and x > self.H:
            return False

        return True

    def pdf(self, x: float):
        if not self.is_inbound(x):
            raise ValueError(f"Requires {self.L} < {x} < {self.H}")

        scaled = x**(-self.alpha-1)
        return self.num_factor*scaled/self.den_factor

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
