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

def construct_rf_chunks(df: pd.DataFrame, lags: int, exog_df: pd.DataFrame = None) -> Tuple[np.ndarray, np.ndarray]:

    if isinstance(df, pd.Series):
        df = df.to_frame()

    if isinstance(exog_df, pd.Series):
        exog_df = exog_df.to_frame()

    add_exog = exog_df is not None

    delta_lags = relativedelta(months=lags) 

    y = df.iloc[lags:]

    N, M = y.shape
    E = exog_df.shape[1] if add_exog else 0

    regr_size = lags*(M + E)

    X = np.empty((N, regr_size))

    for i, date in enumerate(y.index.tolist()):

        regressors = np.empty((1, regr_size))

        prev_date = date - delta_lags
        lagged_values = df.loc[prev_date:date - one_month]

        
        regressors[0, :M*lags] = lagged_values.to_numpy().reshape(1, -1)[0]

        if add_exog:
            lagged_exo = exog_df.loc[prev_date:date - one_month]
            regressors[0, -E*lags:] = lagged_exo.to_numpy().reshape(1, -1)[0]

        X[i] = regressors

    return X, y

def make_quad_loss(alpha: float):
    @make_scorer
    def p_quad_loss(y_hat: np.ndarray, y: np.ndarray) -> np.float:
        e = y_hat - y
        sqr = np.square(e)

        return -np.sum(np.where(e < 0, (1-alpha)*sqr, alpha*sqr))

    return p_quad_loss



# TODO: make lag grid searchable
def make_forecaster(
        df: pd.DataFrame,
        exog_df: pd.DataFrame = None,
        lags: int = 12,
        search_params = {},
        **cv_kwargs
    ):

    X, y = construct_rf_chunks(df, exog_df=exog_df, lags=lags)

    search_params = {**grid_search_over, **search_params}

    rf = RandomForestRegressor()

    clf = GridSearchCV(
        rf, search_params,
        scoring=make_quad_loss(alpha=0.5), 
        **cv_kwargs
    )

    clf.fit(X, y)

    model = clf.best_estimator_   

    def forecaster(X: np.ndarray, exog_outsample: np.ndarray = None) -> np.ndarray: 

        add_exog = exog_outsample is not None and exog_df is not None

        X = X.reshape(1, -1)

        y_hat = {}

        all_prediction = np.array([pred.predict(X)[0] for pred in model.estimators_])
        
        y_hat["lower_bound"] = np.percentile(all_prediction, 2.5, axis = 0)
        y_hat["mean"] = np.mean(all_prediction, axis = 0)
        y_hat["upper_bound"] = np.percentile(all_prediction, 97.5, axis = 0)
        

        return y_hat

    return forecaster
