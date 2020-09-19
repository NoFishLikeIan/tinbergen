import seaborn as sns
import numpy as np
import os

import matplotlib.pyplot as plt

from matplotlib import colors, cm

from pandas import DataFrame, Series
from matplotlib.figure import Figure
from typing import List

sns.set(rc={"figure.figsize": (16, 12)})


def safe_savefig(fig: Figure, figname: str):
    cur_dir = os.getcwd()

    plot_dir =  f"{cur_dir}/plots"

    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    fig.savefig(f"{plot_dir}/{figname}")

def make_n_colors(n: int):
    
    tab = cm.get_cmap("tab10")
    cmap = []

    for tup in zip(range(int(n/2)), reversed(range(int(n/2), n))):
        for i in tup:
            cmap.append(tab(i / n))

    return cmap

def plot_subdf(df: DataFrame, cols: List[str] = [], figname: str = None, mul_axis = False, **kwargs):
    """
    Plot multiple columns with different y-axis.
    Thanks to https://stackoverflow.com/a/50655786

    Parameters
    ----------
    df : DataFrame
    cols : List[str], optional
        by default []
    figname : str, optional
        by default None
    """

    if cols is None: 
        cols = df.columns
    
    N = len(cols)

    if N == 0:
        raise ValueError("No imput column")

    if not figname:
        app = "-".join(cols)
        figname = f"plot-{app}.png"

    fig, ax = plt.subplots()

    if mul_axis:
        colors = make_n_colors(N)
        # First axis
        df.loc[:, cols[0]].plot(label=cols[0], color=colors[0], ax = ax, **kwargs)
        ax.set_ylabel(ylabel=cols[0])
        lines, labels = ax.get_legend_handles_labels()

        for n in range(1, N):
            # Multiple y-axes
            ax_new = ax.twinx()
            ax_new.spines['right'].set_position(('axes', 1 + 0.1 * (n - 1)))
            df.loc[:, cols[n]].plot(ax=ax_new, label=cols[n], color=colors[n % len(colors)], **kwargs)
            ax_new.set_ylabel(ylabel=cols[n])

            # Proper legend position
            line, label = ax_new.get_legend_handles_labels()
            lines += line
            labels += label

        ax.legend(lines, labels, loc=0)

    else:
        df[cols].plot(ax = ax)
    
    safe_savefig(fig, figname)
