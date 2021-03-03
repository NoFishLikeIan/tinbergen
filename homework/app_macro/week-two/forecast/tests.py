import numpy as np
import pandas as pd

from scipy.stats import norm

from .loss import make_quad_loss
from .stats import spectral_density

def db(y: pd.DataFrame, df_forecast: pd.DataFrame, estimated: pd.DataFrame,
        alpha = 0.5, save_tabular = False):

    loss = make_quad_loss(alpha)

    p_values = []
    ts = []

    for col in y.columns:
        y_est = estimated[col]
        var = (spectral_density(y_est)[0]*2*np.pi) / len(y)

        col_y = y[col]
        col_f = df_forecast[f"{col}_mean"]
        col_baseline = df_forecast[f"baseline_{col}"]

        # This is the negative loss, so d is inverted
        d_loss = loss(col_baseline, col_y) - loss(col_f, col_y)

        statistic = d_loss / var
        
        p_values.append(norm.cdf(statistic))
        ts.append(statistic)

    results = pd.DataFrame({"d": ts, "p": p_values}, index = y.columns)

    if save_tabular:
        tab = results.to_latex()
        with open("data/db_tst.txt", "w") as file:
            file.write(tab)

    return results