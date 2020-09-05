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

    model = var_model.VAR(df, dates=df.index, freq="Q")

    if lags > 0:
        print(f"Using given lag order ({lags})...")
        results = model.fit(lags, trend="c", verbose=True)
        
    else:
        print("Finding optimum lag order...")
        results = model.fit(trend="c", maxlags = 15, ic = mode, verbose=True) 

    return results


def plot_var(results, var="FF", folder=""):

    irf = results.irf(10)

    plt.figure()
    irf.plot(impulse=var, stderr_type="mc", figsize=(8, 16))
    plt.savefig(f"plots/{folder}/irf.png")

    fevd = results.fevd(10)

    plt.figure()
    fevd.plot()
    plt.savefig(f"plots/{folder}/fevd.png")
     

if __name__ == "__main__":
    df = import_cee("cee.csv")

    standard_res = var(df, lags = 4)
    plot_var(standard_res, folder="ex-lag")

    standard_res = var(df)
    plot_var(standard_res, folder="aic-lag")

