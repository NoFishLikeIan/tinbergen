import os
import pandas as pd
import seaborn as sns

def_columns = ["consumption_low", "consumption_high", "pH", "v_1", "U"]


def plot_data(directory='out_data', plotting_columns=def_columns):

    filepath = os.path.join(directory, 'results.csv')
    df = pd.read_csv(filepath)

    for column in plotting_columns:
        ax = sns.lineplot(y=column, x='sigma', data=df)
        fig = ax.get_figure()

        fig_path = os.path.join(directory, 'plots', column)

        fig.savefig(f'{fig_path}.png')
        fig.clear()

    total_df = df.set_index('sigma')[["consumption_low", "consumption_high"]]
    ax = sns.lineplot(data=total_df)
    fig = ax.get_figure()

    fig_path = os.path.join(directory, 'plots', 'outplot')

    fig.savefig(f'{fig_path}.png')
    fig.clear()


if __name__ == '__main__':
    plot_data()
