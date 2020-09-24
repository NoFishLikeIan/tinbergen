import numpy as np
import pandas as pd

from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import make_scorer

from dateutil.relativedelta import relativedelta

from typing import Tuple


one_month = relativedelta(months=1)
tscv = TimeSeriesSplit(n_splits=5)

grid_search_over = {
    'max_depth': [10, 20, 30],
    'max_features': ['auto', 'sqrt'],
    'n_estimators': [100, 200, 300]
}

def construct_rf_chunks(df: pd.DataFrame, lags: int) -> Tuple[np.ndarray, np.ndarray]:

    delta_lags = relativedelta(months=lags)

    y = df.iloc[lags:]
    N = y.shape[0]

    X = np.empty((N, lags))

    for i, date in enumerate(y.index.tolist()):
        prev_date = date - delta_lags
        lagged_values = df.loc[prev_date:date - one_month]

        X[i] = lagged_values.to_numpy()

    return X, y

@make_scorer
def p_quad_loss(y_hat: np.ndarray, y:np.ndarray, alpha: float = 0.3) -> np.float:
    e = y_hat - y
    sqr = np.square(e)

    return np.sum(np.where(e < 0, -(1-alpha)*sqr, -alpha*sqr))


# TODO: make lag grid searchable
def rf_forecast(df: pd.Series, lags: int = 12, **cv_kwargs):

    X, y = construct_rf_chunks(df, lags)

    rf = RandomForestRegressor()

    clf = GridSearchCV(rf, grid_search_over, scoring=p_quad_loss, **cv_kwargs)
    clf.fit(X, y)

    model = clf.best_estimator_   

    def forecaster(X: np.ndarray) -> np.ndarray: 
        X = X.reshape(1, lags)

        y_hat = np.zeros(3)

        all_prediction = [pred.predict(X)[0] for pred in model.estimators_]
        
        y_hat[0] = np.percentile(all_prediction, 2.5)
        y_hat[1] = model.predict(X)[0]
        y_hat[2] = np.percentile(all_prediction, 97.5)
        

        return y_hat

    return forecaster
