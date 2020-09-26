import numpy as np
import pandas as pd

from dateutil.relativedelta import relativedelta

from typing import NewType, Callable

Predictor = NewType("Predictor", Callable[[np.ndarray], np.ndarray])

def iterative_forecast(
        predictor: Predictor,
        train: np.ndarray,
        lags: int,
        exog: np.ndarray =None,
        periods: int = 1
    ):
    """
    Runs an iterative forecast, using predictor for periods.
    """
    
    variables = train.columns.tolist()
    
    # Define first period to forecast
    last_day = train.index[-1]
    append_period = last_day - relativedelta(months=lags - 1)
    X = train[append_period:last_day].to_numpy()
    
    y_hat = []
    
    for _ in range(periods):

        forecast = predictor(X.reshape(-1, 1))
        
        X[:-1] = X[1:]
        X[-1] = forecast["mean"]
        
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