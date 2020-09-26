# ---- Main imports

import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from collections.abc import Iterable

# ---- Typing imports

from matplotlib import colors, cm
from statsmodels.graphics import tsaplots

from pandas import DataFrame, Series
from matplotlib.figure import Figure
from typing import List, Dict, Callable, Tuple, NewType

from .latex import np_to_pmatrix

sns.set(rc={"figure.figsize": (16, 12)})

CUR_DIR = os.getcwd()
MATRIX_DIR =  f"{CUR_DIR}/data/matrix"
PLOT_DIR =  f"{CUR_DIR}/plots"

def __safe_savenp(matrix: np.ndarray, filename: str):

    if not os.path.exists(MATRIX_DIR):
        os.makedirs(MATRIX_DIR)

    latex_matrix = np_to_pmatrix(matrix)

    filedir = f"{MATRIX_DIR}/{filename}"

    with open(filedir, "w") as file:
        file.write(latex_matrix)

def __safe_savefig(fig: Figure, figname: str):

    if not os.path.exists(PLOT_DIR):
        os.makedirs(PLOT_DIR)

    fig.savefig(f"{PLOT_DIR}/{figname}")
    fig.clf()

def __make_n_colors(n: int):
    
    tab = cm.get_cmap("tab10")
    cmap = []

    for tup in zip(range(int(n/2)), reversed(range(int(n/2), n))):
        for i in tup:
            cmap.append(tab(i / n))

    return cmap

def plot_subdf(df: DataFrame, cols: List[str] = [], figname: str = None, mul_axis = False, save = False, **kwargs) -> Figure:
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
        colors = __make_n_colors(N)
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
    
    if save:
        __safe_savefig(fig, figname)

    return fig


def plot_covariance(cov: np.ndarray, var_names: List[str], save_data = False, name: str = None, save = False, **sns_kwargs) -> Figure:

    app = "-".join(var_names)
    figname = f"{name}.png" if name else f"cov-{app}.png"
    filename = f"{name}.txt" if name else f"cov-{app}.txt"


    df = DataFrame(cov, index=var_names, columns=var_names)

    fig, ax = plt.subplots()

    extr = np.max(np.abs(cov))

    sns.heatmap(df,
        xticklabels=var_names, yticklabels=var_names, ax = ax, 
        cmap="coolwarm", vmin=-extr, vmax=extr, 
        **sns_kwargs)

    if save:
        __safe_savefig(fig, figname)

    if save_data:
        __safe_savenp(cov, filename)

    return fig

    
# TODO: Abstract the plotting logic
def plot_acf(df: DataFrame, figname: str = None, save = False) -> Figure:
    
    var_names = df.columns.tolist()

    app = "-".join(var_names)
    figname = f"{figname}.png" if figname else f"cov-{app}.png"

    fig, axes = plt.subplots(nrows=len(var_names))
    fig.tight_layout()

    for i, col in enumerate(var_names):
        ax = axes[i]
        tsaplots.plot_acf(df[col], 
            ax = ax, alpha = .05, lags = 40,
            use_vlines=True, title=f"{col} acf"
        )

    if save:
        __safe_savefig(fig, figname)

    return fig


def plot_density(df: DataFrame, density_fn: Callable[[np.ndarray, float], np.ndarray], l: float = None, figname: str = None, save = False) -> Figure:

    var_names = df.columns.tolist()

    app = "-".join(var_names)
    figname = f"{figname}.png" if figname else f"cov-{app}.png"

    fig, ax = plt.subplots()
    fig.tight_layout()

    plot_data = pd.DataFrame()

    for col in var_names:

        densities = density_fn(df[col], l=l)

        col_name = f"{col} density"
        plot_data[col_name] = densities

    density_space = np.linspace(0, 2*np.pi, num=len(plot_data))
    plot_data["Frequency"] = density_space
    plot_data = plot_data.set_index("Frequency")

    sns.lineplot(data = plot_data, ax=ax)

    
    if save:
        __safe_savefig(fig, figname)

    return fig



def plot_var(df_forecast, train, test, variables = [], save = False, figname=None):
    """
    Plots the output of forecast.run.iterative_forecast
    """

    var_names = df_forecast.columns.tolist()

    app = "-".join(var_names)
    figname = f"{figname}.png" if figname else f"cov-{app}.png"

    
    pre_sample = train.iloc[-10:]
    post_sample = test.iloc[:len(df_forecast)]

    N = len(variables)
    
    rows = int(np.floor(np.sqrt(N)))
    columns = int(np.ceil(N/rows))

    fig, axes = plt.subplots(rows, columns)
    
    
    iter_axes = axes.reshape(-1) if isinstance(axes, Iterable) else [axes]

    for i, ax in enumerate(iter_axes):
                
        var_name = variables[i]
        
        sns.lineplot(data=pre_sample, y=var_name, x=pre_sample.index,ax = ax, color ="r", marker = "o")
        sns.lineplot(data=post_sample, y=var_name, x=post_sample.index, ax = ax, color="r", marker = "o")

        ax.axvline(test.index[0], linestyle="--")

        sns.lineplot(data=df_forecast[f"{var_name}_mean"], ax = ax, color="g", linestyle="--", marker = "o")
        sns.lineplot(data=df_forecast[f"{var_name}_lower_bound"], ax = ax, color="b", alpha = 0.5)
        sns.lineplot(data=df_forecast[f"{var_name}_upper_bound"], ax = ax, color="b", alpha = 0.5)

        ax.fill_between(df_forecast.index, df_forecast[f"{var_name}_lower_bound"], df_forecast[f"{var_name}_upper_bound"], alpha=0.2)
        
        ax.set_title(f"Forecast {var_name}")
        
    fig.tight_layout()

    if save:
        __safe_savefig(fig, figname)

    return fig