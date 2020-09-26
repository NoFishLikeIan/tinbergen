import numpy as np
import pandas as pd

from dateutil.relativedelta import relativedelta

from typing import NewType, Callable

Predictor = NewType("Predictor", Callable[[np.ndarray], np.ndarray])

def fit_into_row(first: np.ndarray, second: np.ndarray)-> np.ndarray:
    first_row = first.reshape(-1, 1)
    second_row = second.reshape(-1, 1)

    return np.vstack((first_row, second_row))
    

def iterative_forecast(
        predictor: Predictor,
        train: np.ndarray,
        lags: int,
        exog: np.ndarray = None,
        periods: int = 1
    ):

    """
    Runs an iterative forecast, using predictor for periods.
    """

    add_exog = exog is not None
    
    variables = train.columns.tolist()
    
    # Define first period to forecast
    last_day = train.index[-1]
    append_period = last_day - relativedelta(months=lags - 1)

    endog_X = train[append_period:last_day].to_numpy()

    if add_exog:
        exog_X = exog[append_period:last_day].to_numpy()
        iter_day = last_day
    
    y_hat = []
    
    for _ in range(periods):

        if add_exog:
            X = fit_into_row(endog_X, exog_X)

            # Update the exogenous variable
            exog_X[:-1] = exog_X[1:]
            iter_day = last_day + relativedelta(months=1)
            exog_X[-1] = exog.loc[iter_day]

        else:
            X = endog_X.reshape(-1, 1)

        forecast = predictor(X)
        
        endog_X[:-1] = endog_X[1:]
        endog_X[-1] = forecast["mean"]
        
        y_hat.append(forecast)

    
    end_date = last_day + relativedelta(months=periods)    
    index = pd.date_range(start=last_day, end=end_date, freq="M")
    compact_forecast = pd.DataFrame(y_hat, index = index)
    
    df = pd.DataFrame(index = index)
    
    # Expand columns
    for column in compact_forecast.columns:
        
        expanded_column = compact_forecast[column].apply(pd.Series)
        expanded_column = expanded_column.rename(columns = lambda i: f"{variables[i]}_{column}")
        
        df = pd.concat([df[:], expanded_column[:]], axis=1)
        
            
    return df