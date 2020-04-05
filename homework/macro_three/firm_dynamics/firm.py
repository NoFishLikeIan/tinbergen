import numpy as np
import scipy.optimize as opt
import functools as fn
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

import seaborn as sns
sns.set()

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

            return production - cost - self.fixed_cost

        result = opt.minimize(lambda l: -pi_labour(l), 2, bounds=positive)
        payoff = -result.fun[0]
        labour = result.x[0]

        return payoff, labour


if __name__ == '__main__':
    firm = Firm(10, .7)

    wages = np.linspace(1, 10, 100)
    productivity = np.linspace(1, 100, 100)

    n, m = wages.shape[0], productivity.shape[0]

    labour_surface = np.zeros((n, m))
    payoff_surface = np.zeros((n, m))

    xs, ys = np.meshgrid(wages, productivity)

    for i, w in enumerate(wages):
        for j, a in enumerate(productivity):
            payoff, labour = firm.pi(w, a)
            payoff_surface[i, j] = payoff
            labour_surface[i, j] = labour

    print("Plotting...")

    fig = plt.figure(figsize=(14, 14))
    ax = Axes3D(fig)
    ax.plot_surface(xs, ys, labour_surface.T)
    ax.set_xlabel("wages, w")
    ax.set_ylabel("productivity, a")
    ax.set_zlabel("opt_labour, l")
    plt.savefig("optimal_labor.png")
    plt.close()

    print("Done!")

    print("Plotting...")

    fig = plt.figure(figsize=(14, 14))
    ax = Axes3D(fig)
    ax.plot_surface(xs, ys, payoff_surface.T)
    ax.set_xlabel("wages, w")
    ax.set_ylabel("productivity, a")
    ax.set_zlabel("payoff, l")
    plt.savefig("payoff.png")
    plt.close()
