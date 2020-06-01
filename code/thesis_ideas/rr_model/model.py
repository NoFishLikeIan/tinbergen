import numpy as np
from scipy.integrate import dblquad
from networkx.algorithms.centrality import trophic

from typing import NoReturn, Tuple

from .pareto import MultivariatePareto

default_parameters = {
    "beta": 0.99,
    "delta": 0.05,
    "alpha": 0.5,
    "gamma": 0.6,
    "lambda": 0.1
}


def logit(x, scale=10e5):
    m = np.exp(-x/scale)
    return 1/(1+m)


class Industry:
    def __init__(self,
                 wage=0.5,
                 fixed_overhead=0.5,
                 M=10_000,
                 params={},
                 max_iter=100,
                 n=100,
                 **dist_params):

        self.fixed_overhead = fixed_overhead
        self.M = M
        self.params = {**default_parameters, **params}
        self.wage = wage

        self.params["rho"] = (1-self.params["beta"]) / \
            self.params["beta"] + self.params["delta"]

        dist = MultivariatePareto(**dist_params)

        self.lower_bounds = max(dist.theta_one, dist.theta_two)
        self.n = n

        self.space = np.linspace(self.lower_bounds, 1, n)
        self.sampling_dist = dist
        self.max_iter = max_iter

        self.mus = [np.zeros((n, n))]
        self.t = 0

        self.suppliers = []

    @property
    def fixed_costs(self):
        costs = 0

        for supplier, dep in self.suppliers:

            costs += (1-logit(supplier.aggregate_prod, scale=5e6))*dep

        # print(costs)
        return costs

    @property
    def discount(self):
        R = self.params["rho"] - self.params["delta"]
        return (1-self.params["lambda"])/(1-R)

    @property
    def steady_state(self):
        a, t = np.meshgrid(self.space, self.space)

        return self.prod_decision(a, t)*self.sampling_dist.pdf(a, t)*self.M

    @property
    def mu(self):
        return self.mus[self.t]

    @property
    def aggregate_prod(self):
        """
        TODO: This might be the correct form, for now I am 
        just going to use a simple one.
        y, _ = dblquad(
            lambda a, t: self.production(a, t)*self.mu_at(a, t),
            self.lower_bounds, 1,
            lambda _: self.lower_bounds, lambda _: 1
        )
        """
        A, T = np.meshgrid(self.space, self.space)

        y = self.production(A, T)*self.mu

        return np.sum(y)

    @property
    def trophic_inc(self):
        return trophic.trophic_incoherence_parameter(self.G)

    def optimal_factors(self, prod: float, tau: float) -> Tuple[float, float]:
        net_prod = (self.params["gamma"] - self.params["alpha"])
        den = 1-self.params["gamma"]

        k = np.power(self.params["alpha"]/self.params["rho"], (1-net_prod)/den) * \
            np.power(net_prod/self.wage, net_prod/den) * \
            prod * np.power(1-tau, 1/den)

        l = np.power(prod*(1-tau)*net_prod/self.wage, 1/(1-net_prod)) * \
            np.power(k, self.params["alpha"] /
                     (1-net_prod)) + self.fixed_overhead

        return k, l

    def production(self, prod: float, tau: float) -> float:

        capital, labour = self.optimal_factors(prod, tau)

        capital = (1-tau)*prod*np.power(capital, self.params["alpha"])
        labour = np.power(labour-self.fixed_overhead,
                          self.params["gamma"]-self.params["alpha"])

        return capital*labour

    def costs(self, prod: float, tau: float) -> float:
        capital, labour = self.optimal_factors(prod, tau)

        costs = self.wage*labour + \
            self.params["rho"]*capital + self.fixed_costs

        return costs

    def profit(self, prod: float, tau: float) -> float:

        costs = self.costs(prod, tau)

        production = self.production(prod, tau)

        return production - costs

    def prod_decision(self, prod: float, tau: float) -> np.array:
        pi = self.profit(prod, tau)*self.discount

        return np.where(pi > 0, 1, 0)

    def step(self) -> NoReturn:
        A, T = np.meshgrid(self.space, self.space)

        entrants = self.prod_decision(A, T)\
            * self.sampling_dist.pdf(A, T)*self.M

        prev_mu = self.mus[self.t]
        survivors = (1-self.params["lambda"])*prev_mu

        mu = survivors + entrants

        self.mus.append(mu)

        self.t += 1

    def add_supplier(self, node: 'Industry', dep: float) -> NoReturn:
        self.suppliers.append([node, dep])
