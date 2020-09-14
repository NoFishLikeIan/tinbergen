import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils.read_data import read_data
from utils.plot import plot_series


if __name__ == '__main__':
    
    df = read_data("data/rz.xls", time_name="quarter")
    
    plot_series(df, folder="rz")

    df.to_csv("data/parsed_rz.xls")