import numpy as np
import pandas as pd

from .datetime import months


def find_index(iteree, fn):
    for i, elem in iteree:
        if fn(elem):
            return i

    else:
        return -1


def dummify_for_month(datetime_vector, after_period_dummies=[]):
    months_vector = map(
        lambda datetime: months[datetime.month - 1], datetime_vector)

    month_dummy = pd.get_dummies(months_vector)[
        months].drop(months[-1], axis=1)

    event_dummy = pd.DataFrame(np.zeros((len(datetime_vector), len(after_period_dummies))), index=datetime_vector, columns=[
        f'{month}-{year}'for month, year in after_period_dummies])

    for n, column in enumerate(event_dummy.columns):
        month, year = after_period_dummies[n]
        event_dummy.loc[f'{year}-{month}-{1}':, column] = 1

    variables = [
        'constant',
        *month_dummy.columns.tolist(),
        *event_dummy.columns.tolist()
    ]

    return np.concatenate([month_dummy.values, event_dummy.values], axis=1), variables
