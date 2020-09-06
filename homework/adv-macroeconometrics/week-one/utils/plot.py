import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

def plot_var(results, var="FF", folder="", periods = 15):

    irf = results.irf(periods)

    plt.figure()
    irf.plot(impulse=var, stderr_type="mc", figsize=(8, 16))
    plt.savefig(f"plots/{folder}/irf.png")

    fevd = results.fevd(periods - 10)

    plt.figure()
    fevd.plot()
    plt.savefig(f"plots/{folder}/fevd.png")