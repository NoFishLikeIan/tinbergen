import numpy as np
import pandas as pd
import os

from utils.residual_transformation import autocorrelation

if __name__ == '__main__':

    residual_path = "data/resid.npy"

    if not os.path.isfile(residual_path):
        raise ValueError(f"File {residual_path} not found!")

    resid = np.load(residual_path)

    autocorrelation(resid)
