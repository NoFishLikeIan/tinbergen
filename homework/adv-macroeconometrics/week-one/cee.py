import pandas as pd
import numpy as np

from statsmodels.tsa.vector_ar import var_model

from utils.read_data import read_data
from utils.plot import plot_var


def var(df, lags = -1, mode = 'aic'):

    model = var_model.VAR(df, dates=df.index, freq="Q")

    if lags > 0:
        print(f"Using given lag order ({lags})...")
        results = model.fit(lags, trend="c", verbose=True)
        
    else:
        print("Finding optimum lag order...")
        results = model.fit(trend="c", maxlags = 15, ic = mode, verbose=True) 

    return results

if __name__ == "__main__":
    df = read_data("data/cee.xls")

    standard_res = var(df, lags = 4)
    plot_var(standard_res, folder="ex-lag")

    standard_res = var(df)
    plot_var(standard_res, folder="aic-lag")

