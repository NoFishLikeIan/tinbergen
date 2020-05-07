import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import networkx as nx

from mpl_toolkits import mplot3d
from matplotlib import animation

from rr_model.model import Industry
from rr_model.network import Network


sns.set(rc={'figure.figsize': (12, 8)})


def simulate(net: Network, iters=150, verbose=True, f=2):
    if verbose:
        print("Bringing to steady...")
    net.bring_to_steady(iters=iters, verbose=verbose)
    n = len(net)

    prev_wage = net[n-1].wage
    next_wage = prev_wage*f

    net[n-1].wage = next_wage

    if verbose:
        print(f"Wage: {prev_wage} -> {next_wage}")

    data = [[] for _ in range(n)]

    base = [net[i].aggregate_prod for i in range(n)]

    if verbose:
        print("Shock...")

    for _ in range(iters):
        if verbose:
            print(f"{_+1}/{iters}", end='\r')

        for i in range(n):
            net[i].step()
            prod = net[i].aggregate_prod / base[i]
            data[i].append(prod)

    net[n-1].wage = prev_wage

    if verbose:
        print("...recovery...")

    for _ in range(iters):
        if verbose:
            print(f"{_+1}/{iters}", end='\r')

        for i in range(n):
            net[i].step()
            prod = net[i].aggregate_prod / base[i]
            data[i].append(prod)

    if verbose:
        print("...done!")

    return pd.DataFrame(data).T


if __name__ == '__main__':
    theta_one = 0.2
    overhead = 0.06

    params = {
        "lambda": 0.3,
        "beta": 0.95
    }

    theta_two = [0.2, 0.25, 0.2]
    firms = 3
    inds = []

    for _ in range(firms):

        i = Industry(
            fixed_overhead=overhead,
            alpha=3,
            theta_one=theta_one,
            theta_two=theta_two[_],
            params=params,
        )

        inds.append(i)

    d = np.tril(np.random.randint(1, 10, size=(firms, firms)), -1)

    net = Network(inds, d)

    # nx.draw_networkx(net.G)
    # plt.savefig("plots/network.png")

    df = simulate(net, iters=30, f=1.2)
    df.plot()

    plt.savefig("plots/wage_shock.png")
