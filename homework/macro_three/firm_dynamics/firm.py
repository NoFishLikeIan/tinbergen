import numpy as np
import scipy.optimize as opt
import functools as fn

from typing import Callable, Tuple

from distribution import BoundedParetoDensity

positive = ((0, None),)


def production(labour, prod_draw, gamma):
    out = prod_draw*labour**gamma
    return out


def cost(labour, wage):
    return wage*labour


class Firm:
    def __init__(self, fixed_cost: float = 10, gamma: float = 0.7):
        if gamma > 1:
            raise ValueError("Gamma needs to be < 1")

        self.gamma = gamma
        self.fixed_cost = fixed_cost

    def pi(self, wage: float, prod_draw: float) -> Tuple[float, float]:

        result = opt.minimize(
            lambda l: -production(l, prod_draw, self.gamma) + cost(l, wage),
            0, bounds=positive)

        payoff = -result.fun[0]
        labour = result.x[0]

        return payoff, labour

    def thr_prod(self, wage: float, atol: float = 1e-5):
        productivity = np.linspace(1, 100, 500)
        for draw in productivity:
            payoff, labour = self.pi(wage, draw)

            if payoff - self.fixed_cost < atol:
                return labour
        else:
            raise ValueError("No such threshold, payoff is always positive")


class Market(Firm):
    def __init__(self, cdf, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def N(self):
        return 1

    def output(self, prod_draw: float, labour: float):
        return production(labour, prod_draw, self.gamma)

    def wage_eq(self, prod_draw: float, labour: float):
        result = opt.root(
            lambda w: w - prod_draw * self.gamma * labour**(self.gamma - 1),
            0)

        w = result.x[0]

        return w

    def total_output(self, labour: float, thr: float):
        density = BoundedParetoDensity(L=thr)

        Q = self.N * density.E(lambda a: self.output(a, labour))

        return Q


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set(rc={'figure.figsize': (16, 12)})

    m = Market(10, .7)

    wages = np.linspace(1, 10, 100)
    productivity = np.linspace(1, 100, 100)

    # cd = [firm.thr_prod(w) for w in wages]
#
    # plt.plot(wages, cd)
    # plt.xlabel("wages, w")
    # plt.ylabel("threshold producitivity, cd")
#
    # plt.savefig("plots/q2_cd.png")
