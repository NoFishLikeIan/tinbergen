from rr_model.model import Industry
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from mpl_toolkits import mplot3d
from matplotlib import animation


sns.set(rc={'figure.figsize': (12, 8)})


def plt_3d(X, Y, Z, title='', labels=['', '', ''], cont=False):

    x_label, y_label, z_label = labels

    if cont:
        plt.figure()
        plt.contourf(X, Y, Z, 50,  cmap="jet")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.ylim(min(Y), 0.5)
        plt.title(title)

    else:
        ax = plt.axes(projection='3d')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_zlabel(z_label)
        ax.set_title(title)
        ax.plot_surface(X, Y, Z)

    plt.savefig(f'plots/{title}.png')
    plt.close()


def section_plot(Zs, tau=0.5):

    plt.figure()

    n = len(Zs)
    b = 0.2

    for i, Z in enumerate(Zs):
        alpha = b * (1 + (i+1)/n)
        plt.plot(Z, alpha=alpha, c='blue')

    plt.xlabel("Productivity")
    plt.ylabel("Density")

    plt.title(f"mu(a | tau = {tau}")
    plt.savefig("plots/cross_plot.png")


def animate_line(x, dists, title='', labels=['', '']):
    x_label, y_label = labels

    upper = max((max(i) for i in dists))

    ntime = len(dists)

    fig, ax = plt.subplots(figsize=(12, 8))

    line, = ax.plot(x, dists[0])

    def animate(i):
        line.set_ydata(dists[i])  # update the data.
        return line,

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xlim(0, 1)
    plt.ylim(0, upper)

    plt.rcParams['animation.ffmpeg_path'] = '/mnt/c/Users/andre/ffmpeg/bin/ffmpeg.exe'
    FFwriter = animation.FFMpegWriter(
        fps=10, extra_args=['-vcodec', 'libx264'])

    ani = animation.FuncAnimation(
        fig, animate, ntime, repeat_delay=1_000)

    ani.save('plots/mu_evol.mp4', writer=FFwriter)


def animate_cont(X, Y, convergence, lower=0, title='', labels=['', '', '']):
    x_label, y_label, _ = labels

    ntime = len(convergence)

    fig = plt.figure(figsize=(8, 8), facecolor='w')
    ims = []

    for i in range(ntime):
        im = plt.contourf(
            X, Y, convergence[i], 40, cmap="jet")
        ims.append(im.collections)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.axes().set_aspect('equal')

    plt.xlim(lower, 1)
    plt.ylim(lower, 0.5)

    plt.rcParams['animation.ffmpeg_path'] = '/mnt/c/Users/andre/ffmpeg/bin/ffmpeg.exe'
    FFwriter = animation.FFMpegWriter(
        fps=10, extra_args=['-vcodec', 'libx264'])

    ani = animation.ArtistAnimation(
        fig, ims, repeat_delay=1_000)

    ani.save('plots/evolution.mp4', writer=FFwriter)


if __name__ == '__main__':
    theta_one = 0.2
    theta_two = 0.2
    fixed = 0.02
    overhead = 0.06

    params = {
        "lambda": 0.3,
        "beta": 0.95
    }

    I = Industry(
        fixed_costs=fixed,
        fixed_overhead=overhead,
        alpha=3,
        theta_one=theta_one,
        theta_two=theta_two,
        params=params,
        n=25
    )
    cov = I.sampling_dist.covariance

    Z = I.steady_state

    space = I.space

    plt_3d(space, space, Z, f"cont_mu_steady", labels=[
           "Prod", "Policy", "Mass"], cont=True)

    A, T = np.meshgrid(space, space)

    dist = I.sampling_dist.pdf(A, T)
    pi = I.profit(A, T)

    plt_3d(space, space, dist, f"distribution", labels=[
           "Prod", "Policy", "Mass"], cont=True)

    plt_3d(space, space, pi, f"profit", labels=[
        "Prod", "Policy", "Mass"], cont=True)

    taufive = Z[~np.all(Z == 0, axis=1)]
    section_plot(taufive)
