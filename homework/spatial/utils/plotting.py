import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from mpl_toolkits import mplot3d

sns.set()


def plot_wage_transport(model, Ts=[1.3, 1.5, 1.7, 1.9, 2.1], figsize=(12, 8), save=''):
    lams = np.linspace(0, 1, 100)
    df = pd.DataFrame(index=lams, columns=[f"T {T}" for T in Ts])

    for T in Ts:
        wage_r = []

        for l in lams:
            w1, w2 = model.solve(l, T)[-1]
            ratio = w1 / w2
            wage_r.append(ratio)

        df[f"T {T}"] = wage_r

    df.plot(figsize=figsize)
    plt.ylabel("w1/w2")
    plt.xlabel("lambda")
    plt.title("Variations in transport costs, T")
    plt.hlines(1, xmin=0, xmax=1, linestyle="--")
    plt.xlim(0, 1)

    if len(save) > 0:
        plt.savefig(save)
    else:
        plt.show()

    plt.close()


def plt_3d(X, Y, Z, title='', labels=[], one=False, figsize=(12, 8)):

    x_label, y_label, z_label = labels
    ax = plt.axes(projection='3d', figsize=figsize)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    ax.set_title(title)
    ax.plot_surface(X, Y, Z)

    if one:
        S = np.ones(Z.shape)
        ax.plot_surface(X, Y, S, alpha=1)

    return ax


def plt_countour(X, Y, Z, f=False,
                 title='', labels=[], levels=np.arange(0, 2.25, 0.25/2)):
    x_label, y_label = labels

    fig, ax = plt.subplots()

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    if f:
        cs = ax.contourf(X, Y, Z, levels=levels, cmap="coolwarm")
        fig.colorbar(cs, ax=ax, shrink=0.9)
    else:
        cs = ax.contour(X, Y, Z, levels=levels)
        ax.clabel(cs, inline=1, fontsize=10)

    fig.show()


def triplet_plot(mod, extent=[1, 3.1, 0., 1.01], figsize=(9, 18), **kwargs):

    wr = mod.wage_ratio(**kwargs)
    tom = mod.tomahawk(**kwargs)

    fig, (lax, rax) = plt.subplots(1, 2, figsize=figsize)

    lax.imshow(wr, cmap="coolwarm")
    lax.set_xlabel("T")
    lax.set_ylabel("Lambda")
    lax.set_title("Wage ratio")
    lax.grid(None)

    rax.imshow(tom, cmap="coolwarm", extent=extent)
    rax.set_xlabel("T")
    rax.set_ylabel("Lambda")
    rax.set_title("Pitchfork bifurcation")
    rax.grid(None)

    fig.show()

    return wr, tom
