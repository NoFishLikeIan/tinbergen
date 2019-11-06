import seaborn as sns
import os
import pandas as pd

from src.generator import gen_mean_median_data, asymptotic_std_median


def plot_sample(r: dict):

    for key, record in r.items():
        distplot = sns.distplot(record)

        fig = distplot.get_figure()
        fig.savefig(f'plots/{key}_distplot.png')
        fig.clear()

        print('Saved fig')


def make_table(rec):
    raw_table = pd.DataFrame.from_records(rec).T
    indices = list(raw_table.index)

    records = []
    for key in indices:
        datum = {}
        n, dist, metric = key.split('_')
        datum['n'] = int(n)
        datum['Distribution'] = dist
        datum['Estimator'] = metric

        datum['Standard deviation'] = raw_table['standard_deviation'][key]
        datum['JB test, p-value'] = raw_table['jarque_bera'][key]

        records.append(datum)

    tb = pd.DataFrame.from_records(records).sort_values(['n', 'Estimator'])

    return tb


def plot_std_ev(table, est='mean'):

    ax = sns.lineplot(x='n', y='Standard deviation', hue='Distribution',
                      data=table[table['Estimator'] == est])
    fig = ax.get_figure()
    fig.savefig(f'plots/{est}_sigma.png')
    fig.clear()


def make_tex(table, save_as='table'):
    st = table.to_latex(index=False)
    with open(f'data/{save_as}.tex', 'w') as file:
        file.write(st)


def make_median_std_table(samples):
    std_tuples = (asymptotic_std_median(sample)
                  for sample in samples)
    normal, student = zip(*std_tuples)

    df = pd.DataFrame(index=samples)
    df['normal'] = normal
    df['t'] = student
    return df


if __name__ == "__main__":
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    samples = [10, 25, 100, 500]

    rec, sampled_data = gen_mean_median_data(
        samples=samples, replications=1000, save=True)

    table = make_table(rec)

    median_v_df = make_median_std_table(samples)

    plot_std_ev(table, est='mean')
    plot_std_ev(table, est='median')
    plot_sample(sampled_data)
    make_tex(median_v_df, save_as='median_theoretical_v')
    make_tex(table)

    print(table)
    print('done')
