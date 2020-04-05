import math


def opt_n(c: float):
    a = math.sqrt(1 + 4/c)

    remainder = math.atan(1/math.tan(math.pi*(1+a)))

    return a - 0.5 + remainder/math.pi


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    sns.set(rc={'figure.figsize': (10, 8)})

    partitions = 1000
    c_space = [n/partitions for n in range(1, partitions)]

    optimal_n = []

    for n, c in enumerate(c_space):
        optimal_n.append(opt_n(c))
        print(f'Progress: {n}/{len(c_space)}', end='\r')

    optimal_n = pd.Series(optimal_n, index=c_space)

    if True:
        sns_plot = sns.lineplot(data=optimal_n)

        sns_plot.set(xlabel='c', ylabel='Optimal N')

        sns_plot.get_figure().savefig('Optimal_n.png')
