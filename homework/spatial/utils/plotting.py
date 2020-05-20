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
    tom = mod.tomahawk()

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


def pitchfork(mod, extent=[1, 3.1, 0., 1.01], figsize=(9, 18), **kwargs):
    wr = mod.wage_ratio(**kwargs)
    tom = mod.tomahawk()

    fig, ax = plt.subplots(figsize=figsize)

    ax.imshow(tom, cmap="coolwarm", extent=extent)
    ax.set_xlabel("T")
    ax.set_ylabel("Lambda")
    ax.set_title("Pitchfork bifurcation")
    ax.grid(None)

    fig.show()

    return wr, tom


def sustain_break_plot(mod, T=np.linspace(1, 2.5, 150), figsize=(16, 12)):
    g = mod.g(T)
    f = mod.f(T)

    s = mod.sustain_p
    b = mod.break_p

    df = pd.DataFrame(index=T)
    df["g(T)"] = g
    df["f(T)"] = f

    fig, ax = plt.subplots(figsize=figsize)
    df.plot(ax=ax, lw=2)

    ax.axhline(1, linestyle='--')
    ax.axvline(s, linestyle='--', c='k')
    ax.axvline(b, linestyle='--', c='k')

    ax.plot(s, 1, 'ko', markersize=12)
    ax.plot(b, 1, 'ko', markersize=12)

    sus_label = f'Sustain point, T={s:.3}'
    break_label = f'Break point, T={b:.3}'

    ax.text(s - 0.05, 1.05, "A", fontsize=16)
    ax.text(b + 0.05, 1.05, "B", fontsize=16)
    ax.text(s - 0.05, 0.3, sus_label, horizontalalignment='right')
    ax.text(b + 0.05, 0.3, break_label)

    ax.set_xlim(T[0], T[-1])
    ax.set_xlabel("Transport costs, T")

    return fig, ax


def welfare_plot(model, n=100):
    lams = np.linspace (0.01,1,n)

    y = np.zeros(n)
    z = np.zeros(n)
    w = np.zeros(n)

    # real income
    u1m = np.zeros(n)
    u1a = np.zeros(n)
    u2m = np.zeros(n)
    u2a = np.zeros(n)

    # real wages
    v1m = np.zeros(n)
    v1a = np.zeros(n)
    v2m = np.zeros(n)
    v2a = np.zeros(n)

    i = 0
    for lam in np.nditer(lams):
        result = model.welfare(lam, T)
        y[i] = result[0]
        z[i] = result[1][0]
        w[i] = result[1][1]
        u1m[i] = result[2][0]
        u1a[i] = result[2][1]
        u2m[i] = result[2][2]
        u2a[i] = result[2][3]
        v1m[i] = result[3][0]
        v1a[i] = result[3][1]
        v2m[i] = result[3][2]
        v2a[i] = result[3][3]

        i += 1
        
    fig = plt.figure()
    title = 'Welfare changes as a function of $\u03BB$, $\u03C6$ = '+ str(phi)
    fig.suptitle(title)

    fig1 = fig.add_subplot(131)
    fig1.plot(lams,y)
    fig1.set_title('Total welfare changes')
    fig1.set_xlabel('$\u03BB$')
    fig1.set_ylabel('Total real income')

    fig2 = fig.add_subplot(132)
    labels = [
        'Real income region 1',
        'Real income region 2'
    ]
    Y = np.vstack([z,w])
    fig2.stackplot(lams,Y, labels = labels)
    fig2.set_title('Regional welfare composition')
    fig2.set_xlabel('$\u03BB$')
    fig2.set_ylabel('Real income')
    fig2.legend()

    fig3 = fig.add_subplot(133)
    labels = [
        'Region 1 - manufacturing',
        'Region 1 - agriculture',
        'Region 2 - manufacturing',
        'Region 2 - agriculture'
    ]
    Y = np.vstack([u1m,u1a,u2m,u2a])
    fig3.stackplot(lams,Y, labels = labels)
    fig3.set_title('Sectoral welfare composition')
    fig3.set_xlabel('$\u03BB$')
    fig3.set_ylabel('Real income')
    fig3.legend()
    plt.savefig('welfare1.png')

    g = plt.figure()
    g1 = g.add_subplot(121)

    g1.plot(lams, u1m, label="Region 1 - manufacturing")
    g1.plot(lams, u2m, label="Region 2 - manufacturing")
    g1.plot(lams, u1a,"--", label='Region 1 - agriculture')
    g1.plot(lams, u2a,"--", label='Region 2 - agriculture')
    g1.set_title('Welfare changes')
    g1.set_xlabel('$\u03BB$')
    g1.set_ylabel('Real income')
    g1.legend()

    g2 = g.add_subplot(122)

    g2.plot(lams, v1m, label="Region 1 - manufacturing")
    g2.plot(lams, v2m, label="Region 2 - manufacturing")
    g2.plot(lams, v1a,"--", label='Region 1 - agriculture')
    g2.plot(lams, v2a,"--", label='Region 2 - agriculture')
    g2.set_title('Welfare changes')
    g2.set_xlabel('$\u03BB$')
    g2.set_ylabel('Real wages')
    g2.legend()
    g.savefig('welfare2.png')