import numpy as np
import pandas as pd
import calendar
import os

from itertools import product
from functools import partial
from datetime import datetime

from .iter_fns import compute_percentage_difference, map_product
from .datetime import months, get_month_index


def shift_column(df):
    '''
    Recursively shift dataframe column downwards, until no "Unnamed:" column is present
    '''
    parsed_df = df.copy()

    if any(('Unnamed:' in col for col in parsed_df.columns)):
        parsed_df.columns = parsed_df.iloc[0]
        parsed_df = parsed_df.iloc[1:]

        return shift_column(parsed_df)

    else:
        return parsed_df.reset_index(drop=True)


def get_from_df(df, index, column, default=None):
    '''
    Safely get from dataframe
    '''
    if column in df.columns and index in df.index:
        return df[column][index]
    else:
        return default


def make_date_price_tuple(df, year, month):
    numerical_month = get_month_index(month) if type(month) == str else month
    return (datetime(year=year, month=numerical_month, day=1), get_from_df(df, year, month))


def csv_to_vector(data_path, time_column='Period', index_filter=None, cache=True, caching_file='cached/inflation_matrix.npy'):
    if cache and os.path.isfile(caching_file):
        print('Loading cached data...')
        try:
            mtrx = np.load(caching_file)
            return mtrx[:, 0], mtrx[:, 1]
        except ValueError as error:
            print('Not able to load file', error)
            print('Continue...')

    df = pd.read_csv(data_path)
    df[time_column] = pd.to_datetime(df[time_column], format='%Y/%M')
    df = df.set_index(time_column)
    filtered_df = df.loc[f'{index_filter}-01-01':]

    inflation_pct = compute_percentage_difference(filtered_df['SA0'].tolist())
    datetimes_vector = filtered_df.index.tolist()

    if cache:
        print('Saving data to cache...')
        np.save(caching_file, np.vstack(
            [datetimes_vector, inflation_pct]), allow_pickle=True)

    return np.array(datetimes_vector), np.array(inflation_pct)


def xlsx_to_vector(data_path, time_column='Year', months=months, index_filter=None, cache=True, caching_file='cached/inflation_matrix.npy'):
    '''
    Read inflation series and return two vectors, dates and percentage inflation
    '''

    if cache and os.path.isfile(caching_file):
        print('Loading cached data...')
        try:
            mtrx = np.load(caching_file)
            return mtrx[:, 0], mtrx[:, 1]
        except ValueError as error:
            print('Not able to load file', error)
            print('Continue...')

    raw_df = pd.read_excel(data_path).dropna(
        axis=0, how='any')

    df = shift_column(raw_df)

    if not time_column or time_column not in df.columns:
        raise KeyError(f'Not valid date column: {time_column}')

    years = df[time_column].tolist()

    df = df.set_index(time_column)
    filtered_df = df.loc[index_filter:]

    tuplify_data = partial(make_date_price_tuple, filtered_df)
    datetimes, prices = map_product(tuplify_data, years, months)

    inflation_pct = compute_percentage_difference(prices)

    datetimes_vector = np.array(datetimes)[1:]
    inflation_vector = np.array(inflation_pct)

    if cache:
        print('Saving data to cache...')
        np.save(caching_file, np.vstack(
            [datetimes_vector, inflation_vector]), allow_pickle=True)

    return np.array(datetimes_vector), np.array(inflation_pct)
