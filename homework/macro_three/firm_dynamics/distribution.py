
from scipy import integrate
import numpy as np


from utils import functionify


class BoundedParetoDensity:
    def __init__(self, alpha: float = 3, L: float = None, H: float = None):
        one_none = H is None or L is None

        if not one_none and H < L:
            raise ValueError(
                "The lower bound has to be smaller than the upper bound")

        den_scaler = (L/H)**alpha if H is not None else 0

        self.alpha = alpha
        self.L = L
        self.H = H

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

    def E(self, factor: float = None):
        fn_modifier = functionify(factor)

        lower = -np.inf if self.L is None else self.L
        upper = np.inf if self.H is None else self.H

        expected_value, _ = integrate.quad(
            lambda x: fn_modifier(x)*self.pdf(x),
            lower,
            upper
        )

        return expected_value


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np
    xs = np.linspace(1.001, 4, 100)
    dens = BoundedParetoDensity(2, 1, None)

    ys = [dens.pdf(x) for x in xs]
    plt.plot(xs, ys)
    plt.savefig("dens.png")
