import numpy as np
import scipy.optimize as opt
import functools as fn

positive = ((0, None),)


class Firm:
    def __init__(self, fixed_cost: float = 10, gamma: float = 0.7):
        if gamma > 1:
            raise ValueError("Gamma needs to be < 1")

        self.gamma = gamma
        self.fixed_cost = fixed_cost

    def pi(self, wage: float, prod_draw: float):

        def pi_labour(labour: float) -> float:
            production = prod_draw*labour**(self.gamma)
            cost = wage*labour

            return production - cost

        result = opt.minimize(lambda l: -pi_labour(l), 0, bounds=positive)
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


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set(rc={'figure.figsize': (16, 12)})

    firm = Firm(10, .7)

    wages = np.linspace(1, 10, 100)
    productivity = np.linspace(1, 100, 100)

    cd = [firm.thr_prod(w) for w in wages]

    plt.plot(wages, cd)
    plt.xlabel("wages, w")
    plt.ylabel("threshold producitivity, cd")

    plt.savefig("plots/q2_cd.png")
