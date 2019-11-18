import os

import pandas as pd
import seaborn as sns


relative_price_columns = ['p_hh', 'p_hl', 'p_ll', 'p_lh']
security_columns = relative_price_columns + ['arrow_high', 'arrow_low']


def get_data(directory='out_data'):

    filepath = os.path.join(directory, 'results.csv')
    df = pd.read_csv(filepath, index_col=0).set_index('sigma')

    return df


def compute_prices(pH, beta):
    '''
    Returns (pH|H, pH|L, pL|L, pL|H)
    '''
    constant_p = beta / 2
    series = [constant_p, constant_p * pH, constant_p, constant_p * (1 / pH)]

    return pd.Series(series, index=relative_price_columns)


def compute_securities(df, beta=0.95):

    df['arrow_high'] = df['consumption_high'].apply(lambda c: c - 1)
    df['arrow_low'] = df['consumption_low'].apply(lambda c: c - 0.5)

    relative_price_df = df['pH'].apply(
        lambda price: compute_prices(price, beta))

    return pd.concat([df, relative_price_df], axis=1)


def plot_securities(securities_df, columns=security_columns, directory='out_data'):
    df = securities_df.reset_index()

    for column in columns:
        ax = sns.lineplot(y=column, x='sigma', data=df)
        fig = ax.get_figure()

        fig_path = os.path.join(directory, 'plots', column)

        fig.savefig(f'{fig_path}.png')
        fig.clear()

    fig.clear()


if __name__ == '__main__':
    df = get_data()
    securities_df = compute_securities(df)
    plot_securities(securities_df)
