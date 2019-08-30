import numpy as np
import pandas as pd

import constants

from utils.clean import csv_to_vector
from utils.dummify import dummify_for_month


def main():
    datetime_vector, prices_vector = csv_to_vector(
        constants.inflation_series_path,
        cache=False,
        index_filter=constants.start_year
    )

    dummy_matrix, variables = dummify_for_month(
        datetime_vector, after_period_dummies=constants.events_dummies)
    ones = np.ones((dummy_matrix.shape[0], 1))

    X = np.concatenate([ones, dummy_matrix], axis=1)
    betas, residuals, _, _ = np.linalg.lstsq(
        prices_vector.reshape(-1, 1), X)

    result = pd.DataFrame({
        'variables': variables,
        'betas': betas.tolist()[0],
        'residuals': residuals.tolist(),
    }).set_index('variables')

    print(result)


if __name__ == '__main__':
    main()
