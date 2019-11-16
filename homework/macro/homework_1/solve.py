import scipy.optimize as op
import numpy as np

from utils.equilibrium_constraint import budget_constraint
from utils.multipliers_constraints import high_constraint
from utils.consumption import consumptions
from utils.loss import squared_loss
from utils.callback import callback_on_crack


def system_factory(sigma_1, sigma_2):
    def system_equations(parameters):
        v_1, pH = parameters

        if v_1 < 0 or pH < 0:
            return 10, 10

        multiplier_constraint = high_constraint(v_1, sigma_1, sigma_2, pH) - 2
        budget = budget_constraint(v_1, sigma_1, sigma_2, pH) - 0.5

        return multiplier_constraint, budget

    return system_equations


def solver_factory(sigma_1, sigma_2):
    system_of_equations = system_factory(sigma_1, sigma_2)

    def solver(guess):
        return op.fsolve(system_of_equations, guess)

    return solver, system_of_equations


if __name__ == '__main__':
    import seaborn as sns
    import pandas as pd

    sigma_1 = 2

    result = []
    sigma_space = np.linspace(2., 10.)

    for sigma_2 in sigma_space:

        solver, system = solver_factory(sigma_1, sigma_2)

        guess = np.random.uniform(0.1, 1.5, size=2)

        v_1, pH = solver(guess)

        print('Solution, ', v_1, pH)
        low, high = consumptions(v_1, pH, sigma_1, sigma_2)

        result.append([low, high, pH, v_1])

    columns = ['consumption_low', 'consumption_high', 'pH', 'v_1']
    df = pd.DataFrame(result, columns=columns)
    df.index = sigma_space
    list_data = [df[column] for column in columns]

    ax = sns.lineplot(data=list_data)
    fig = ax.get_figure()
    fig.savefig('out_data/output.png')

    df.to_csv('out_data/results.csv')
