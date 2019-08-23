import numpy as np


def value_option(option):
    return lambda S, K: max(S - K if option == 'call' else K - S, 0)


def up_down(delta_t, volatility):
    u = np.exp(volatility * np.sqrt(delta_t))

    return u, 1 - u


def probabilities(delta_t, volatility, interest_rate):
    u, d = up_down(delta_t, volatility)

    p = (np.exp(interest_rate * delta_t) - d) / (u - d)

    return p, 1 - p, u, d
