import numpy as np
from scipy.integrate import dblquad


class MultivariatePareto:
    def __init__(self, alpha, theta_one, theta_two):

        if alpha < 2:
            raise ValueError("Requires alpha > 2")

        self.alpha = alpha
        self.theta_one = theta_one
        self.theta_two = theta_two

    @property
    def theta_prod(self):
        return self.theta_one*self.theta_two

    @property
    def scale_constant(self):
        one_alph = self.alpha + 1

        return one_alph*self.alpha*np.power(self.theta_prod, one_alph)

    def pdf(self, x, y):

        factor = self.theta_two*y + self.theta_one*x - self.theta_prod

        return self.scale_constant / np.power(factor, self.alpha + 2)

    @property
    def covariance(self):
        return self.theta_prod / (np.power(self.alpha - 1, 2) * (self.alpha - 2))


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from mpl_toolkits import mplot3d

    for i in [-5, -4, -2, 2, 4, 5]:

        prods = np.linspace(0, 1, 100)
        taus = np.linspace(0, 1, 100)

        x, y = np.meshgrid(prods, taus)

        p = MultivariatePareto(3, 3, i)

        z = p.pdf(x, y)

        ax = plt.axes(projection='3d')

        ax.set_title(f"{i}")
        ax.plot_surface(x, y, z)

        plt.savefig(f"{i}")
        plt.close()
