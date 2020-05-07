from rr_model.model import Industry
from rr_model.network import Network
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from mpl_toolkits import mplot3d
from matplotlib import animation


sns.set(rc={'figure.figsize': (12, 8)})


if __name__ == '__main__':
    theta_one = 0.2
    overhead = 0.06

    params = {
        "lambda": 0.3,
        "beta": 0.95
    }

    first = Industry(
        fixed_overhead=overhead,
        alpha=3,
        theta_one=theta_one,
        theta_two=0.3,
        params=params,
    )

    second = Industry(
        fixed_overhead=overhead,
        alpha=3,
        theta_one=theta_one,
        theta_two=0.3,
        params=params,
    )

    third = Industry(
        fixed_overhead=overhead,
        alpha=3,
        theta_one=theta_one,
        theta_two=0.3,
        params=params,
    )

    d = np.array([
        [0, 0.2, 0],
        [0, 0, 0],
        [0.2, 0.8, 0]
    ])

    G = Network([first, second, third], d)
