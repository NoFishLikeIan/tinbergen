import numpy as np
import scipy.optimize as opt

from utils.array import stability_equil
from utils import plotting


class TwoRegionModel:
    """
    Simple class that implements the equations given above
    and uses the solution method of Brakman et al. 2009
    """

    def __init__(self,
                 delta=0.4,
                 eps=5.,
                 L=1.,
                 phi=0.5,
                 normalized=False,
                 gamma=None,
                 sigma=1e-4, max_iter=10_000, verbose=0):

        self.delta = delta
        self.eps = eps
        self.L = L
        self.phi = phi
        self.sigma = sigma

        self.max_iter = max_iter
        self.verbose = verbose > 0
        self.normalized = normalized

        self.rho = (eps-1)/eps
        self.gamma = self.delta if gamma is None else gamma
        self.beta = self.rho
        self.alpha = (self.gamma*self.L) / self.eps

    @property
    def fact_I(self):
        if self.normalized:
            return 1

        disc = self.beta / self.rho
        lab = (self.gamma*self.L)/(self.alpha*self.eps)
        exp = 1/(1-self.eps)

        return disc*np.power(lab, exp)

    @property
    def fact_W(self):
        if self.normalized:
            return 1

        disc = self.rho/np.power(self.beta, self.rho)
        lab = self.delta / ((self.eps-1)*self.alpha)

        return disc*np.power(lab, 1/self.eps)

    def converged(self, c, p):
        return (c-p)/c < self.sigma

    def Y(self, w1, w2, lam):
        y1 = self.delta * lam * w1 + (1-self.delta)*self.phi
        y2 = self.delta * (1-lam) * w2 + (1-self.delta)*(1-self.phi)

        return y1, y2

    def W(self, y1, y2, i1, i2, T):
        i1_weight = np.power(i1, self.eps-1)
        i2_weight = np.power(i2, self.eps-1)
        T_weight = np.power(T, 1-self.eps)

        w1 = np.power(y1*i1_weight + y2*i2_weight*T_weight, 1/self.eps)
        w2 = np.power(y1*i1_weight*T_weight + y2*i2_weight, 1/self.eps)

        return self.fact_W*w1, self.fact_W*w2

    def I(self, w1, w2, lam, T):
        rho = 1/(1-self.eps)

        w1_weight = np.power(w1, 1-self.eps)
        w2_weight = np.power(w2, 1-self.eps)
        T_weight = np.power(T, 1-self.eps)

        i1 = np.power(lam*w1_weight + (1-lam)*T_weight*w2_weight, rho)
        i2 = np.power(lam*w1_weight*T_weight + (1-lam)*w2_weight, rho)

        return self.fact_I*i1, self.fact_I*i2

    def solve(self, lam, T):
        """
        Solve the model for a given lambda and transportation cost.

        Returns a list of
        [(Wage 1, Wage 2), (Output 1, Output 2), (Income 1, Income 2), (Real wage 1, Real wage 2)]
        """
        i = 1
        w1 = 1.
        w2 = 1.

        while i < self.max_iter:
            y1, y2 = self.Y(w1, w2, lam)
            i1, i2 = self.I(w1, w2, lam, T)
            nw1, nw2 = self.W(y1, y2, i1, i2, T)

            if self.converged(nw1, w1) and self.converged(nw2, w2):
                if self.verbose:
                    print(f'Converged at iteration {i}')

                real1 = nw1/np.power(i1, self.delta)
                real2 = nw2/np.power(i2, self.delta)

                solution = [
                    (nw1, nw2), (y1, y2), (i1, i2), (real1, real2)
                ]
                return solution

            w1 = nw1
            w2 = nw2

            i += 1
            if self.verbose:
                print(f'Iteration: {i}/{self.max_iter}', end='\r')
        else:
            if self.verbose:
                print(
                    f'Solution did not converge with {self.max_iter} iterations')

    def wage_ratio(self, T=np.linspace(1, 3.1, 150), relative=False):
        lams = np.linspace(0, 1, 101)

        @np.vectorize
        def wage_ratio(l, t):

            w1, w2 = self.solve(l, t)[-1]
            ratio = w1 / w2

            if relative and l > 0.5:
                return 1/ratio

            return ratio

        l, t = np.meshgrid(lams, T)
        wr = wage_ratio(l, t)

        return wr.T

    def tomahawk(self, T=np.linspace(1, 3.1, 200)):
        """
        Given a space for T, produce the data of the 

        """
        wr = self.wage_ratio(T=T)
        tom = np.zeros(wr.shape)
        n = tom.shape[1]

        for col in range(n):

            vec = wr[:, col]
            equil_points, gradients = stability_equil(vec)

            stable = np.where(gradients < 0)
            unstable = np.where(gradients > 0)

            tom[equil_points[stable], col] = -1
            tom[equil_points[unstable], col] = 1

        return tom

    def f(self, T):
        Y1 = (1+self.delta)/2
        Y2 = (1-self.delta)/2

        first = Y1*np.power(T, -(self.rho + self.delta) * self.eps)
        second = Y2*np.power(T, (self.rho - self.delta) * self.eps)

        return first + second

    def g(self, T):
        scaled_T = np.power(T, 1 - self.eps)
        first = (1 - scaled_T)/(1 + scaled_T)

        sq_delta = np.power(self.delta, 2)

        second = self.delta*(1+self.rho)/(sq_delta + self.rho)

        return first + 1 - second

    @property
    def sustain_p(self):
        sol = opt.root(lambda T: self.g(T) - 1, 1.5)

        return sol.x[-1]

    @property
    def break_p(self):
        sol = opt.root(lambda T: self.f(T) - 1, 1.5)

        return sol.x[-1]


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from time import time

    tom_plot = False

    delta = 0.45
    rho = 0.8

    eps = 1 / (1-rho)

    mod = TwoRegionModel(delta=delta, eps=eps)

    if tom_plot == True:
        wr = mod.wage_ratio()

        start = time()
        tom = mod.tomahawk()
        end = time()

        plotting.plot_wage_transport(mod, save="plots/cross.png")

        print("Tom took, ", end-start, " seconds")

        plt.imshow(wr, cmap="coolwarm")
        plt.savefig("plots/wr.png")
        plt.close()

        plt.imshow(tom, cmap="coolwarm", extent=[1, 3.1, 0., 1.01])
        plt.xlabel("T")
        plt.ylabel("Lambda")
        plt.savefig(f"plots/tom.png")
        plt.close()

    fig, ax = plotting.sustain_break_plot(mod)

    fig.savefig("plots/sb_plot.png")
