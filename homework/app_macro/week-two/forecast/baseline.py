import numpy as np
import pandas as pd

from statsmodels.tsa.ar_model import AutoReg
from dateutil.relativedelta import relativedelta


def AR1(data: pd.DataFrame):

    if isinstance(data, pd.Series):
        data = data.to_frame()

    variables = data.columns.tolist()
    first_date = data.index[-1]

    predictors = []

    for column in variables:

        res = AutoReg(data[column], lags=1).fit()
        predictors.append(res)


    def forecast(periods: int):
        end_date = first_date + relativedelta(months=periods)
        column_names = [f"baseline_{var}" for var in variables]

        ar_df = pd.DataFrame(columns=column_names)

        for column, res in zip(column_names, predictors):
            out_sample = res.predict(start = first_date, end = end_date)

            ar_df[column] = out_sample

        return ar_df

    return forecast