import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


def plot_var(results, var="FF", folder="", periods = 15, fevd=True):

    path = f"plots/{folder}"

    if not os.path.exists(path):
        os.makedirs(path)

    irf = results.irf(periods)

    plt.figure()
    irf.plot(impulse=var, stderr_type="mc", figsize=(8, 16))
    plt.savefig(f"{path}/irf.png")
    plt.close()

    if fevd:
        fevd = results.fevd(periods - 10)

        plt.figure()
        fevd.plot()
        plt.savefig(f"{path}/fevd.png")
        plt.close()

    res, corr = results.resid, results.resid_corr

    if type(res) != pd.DataFrame:
        res = pd.DataFrame(res, columns = results.names)

    np.fill_diagonal(corr, 0.)

    if "D" in res.columns:
        res = res.drop("D", axis = 1)

    fig, (ax_plot, ax_cor) = plt.subplots(nrows=1, ncols=2, figsize=(16, 10))
    res.plot(ax = ax_plot)
    ax_plot.set_title("Residuals time series")

    ax_cor.matshow(
        corr, cmap="coolwarm", clim=(-1, 1)
    )

    ax_cor.set_title("Residuals correlation matrix")

    fig.savefig(f"{path}/res.png")