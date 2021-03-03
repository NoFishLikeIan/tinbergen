import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

import warnings

from statsmodels.tools.sm_exceptions import ConvergenceWarning
warnings.simplefilter('ignore', ConvergenceWarning)

sns.set()

def grid(n):
    columns = np.ceil(np.sqrt(n))
    rows = np.ceil(n / columns)
    return int(rows), int(columns)

def plot_series(df, folder = ""):
    path = f"plots/{folder}"

    if not os.path.exists(path):
        os.makedirs(path)

    variables = df.columns
    rows, columns = grid(len(variables))

    fig, axes = plt.subplots(rows, columns, figsize=(15, 15))

    for i, var in enumerate(variables):
        c = int(i/rows)
        r = i % rows 
        ax = axes[c, r]
        ax.set_title(f"{var}")

        df[var].plot(ax = ax)
    
    fig.savefig(f"{path}/ts")

def plot_var(results, impulse, response=[], folder="", periods = 15, fevd=True, plot_stderr=True, autocorr=False):

    path = f"plots/{folder}"

    if not os.path.exists(path):
        os.makedirs(path)

    res, corr = results.resid, results.resid_corr

    if type(res) != pd.DataFrame:
        res = pd.DataFrame(res, columns = results.names)

    
    variables = list(res.columns)

    irf = results.irf(periods)
    
    plot_args = {
        "impulse": impulse,
        "plot_stderr": plot_stderr,
        "stderr_type": "mc",
        "repl": 1_000

    }

    if len(response) == 0:
        response = variables

    for var in response:
        try:
            fig = irf.plot(response=var, **plot_args, orth=True)
        except ValueError:
            fig = irf.plot(response=var, **plot_args, orth=False)

        fig.savefig(f"{path}/irf-{var}.png")

    if autocorr:
        for var in variables:
            fig = sm.graphics.tsa.plot_acf(res[var])
            fig.savefig(f"{path}/autocorr-{var}")

    if fevd:
        fevd = results.fevd()

        plt.figure()
        fevd.plot(figsize=(20, 20))
        plt.savefig(f"{path}/fevd.png")
        plt.close()


    np.fill_diagonal(corr, 0.)

    if "D" in variables:
        res = res.drop("D", axis = 1)

    fig, (ax_plot, ax_cor) = plt.subplots(nrows=1, ncols=2, figsize=(16, 10))
    res.plot(ax = ax_plot)
    ax_plot.set_title("Residuals time series")

    print("corr:", corr)
    ax_cor.matshow(
        corr, cmap="coolwarm", clim=(-1, 1)
    )

    ax_cor.set_xticklabels(['']+variables)
    ax_cor.set_yticklabels(['']+variables)

    ax_cor.set_title("Residuals correlation matrix")

    fig.savefig(f"{path}/res.png")