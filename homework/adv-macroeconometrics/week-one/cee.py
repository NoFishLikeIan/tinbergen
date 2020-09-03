import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from statsmodels.tsa.vector_ar import var_model

sns.set()

def import_cee(name):
    df = pd.read_csv(name).dropna(axis = 1).rename(columns={"Unnamed: 0": "t"})

    qs = df["t"].apply(
        lambda q: "-Q".join([str(int(n)) for n in q.split(":")])
    )

    df["t"] = pd.PeriodIndex(qs.values, freq = "Q")

    return df.set_index("t")


def var(df, lags = -1, mode = 'aic'):
    model = var_model.VAR(df)

    results = model.fit(maxlags = 15, ic = mode) if lags < 1 else model.fit(lags)
    
    return results

def irf_plot(results, var = "FF"):
    irf = results.irf(10)

    plt.figure()
    irf.plot(impulse=var, orth=False)
    plt.savefig(f"plots/irf-{var}.png")

        
     

if __name__ == "__main__":
    df = import_cee("cee.csv")


    r = var(df, lags = 4)
    irf_plot(r)