from utils.finance import value_option, probabilities

interest_rate = .02
volatility = 0.3
strike = 100
S_0 = strike * .75


def evolver_factory(delta_t):
    def evolve_price(S):
        p, 1-p, u, d = probabilities(delta_t, volatility, interest_rate)
        return


def simulate_prices():
    pass
