import pandas as pd
import numpy as np

from utils.read_data import read_data
from utils.plot import plot_var
from utils.var import var

# FIXME: fix parsing warning
pd.options.mode.chained_assignment = None 

def parse_data(df):
    deflator = df["PGDP"]
    population = df["POP"]

    # This assumes PGDP and POP are the last two columns
    target_cols = df.columns[:-2]
    scaled_df = df[target_cols]

    for col in target_cols:
        real = 100 * df[col] / deflator 
        real_pc = real / population
        log = np.log(real_pc)

        scaled_df[col] = log

    scaled_df["D"] = np.zeros(len(scaled_df))
    scaled_df["D"]["1975Q2"] = 1

    scaled_df = scaled_df.rename(
        columns = {
            "GCN": "G",
            "TAX": "T",
            "GDP": "Y"
        }
    )

    return scaled_df



if __name__ == "__main__":
    df = read_data("data/bp.xls")
    scaled_df = parse_data(df)

    results = var(scaled_df,  lags=4, trend="ctt")
    plot_var(results, var="G", folder="bp")
