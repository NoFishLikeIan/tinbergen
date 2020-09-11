import pandas as pd
import numpy as np

from utils.read_data import read_data
from utils.plot import plot_var
from utils.var import var, svar

# FIXME: fix parsing warning
pd.options.mode.chained_assignment = None 

A = np.array([
    [1., 0., "E"],
    ["E", 1., "E"],
    ["E", "E", 1.],
])

B = np.array([
    ["E", 0., 0.],
    [0., "E", 0.],
    [0., 0., "E"]
])

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

    scaled_df = scaled_df.rename(
        columns = {
            "GCN": "G",
            "TAX": "T",
            "GDP": "Y"
        }
    )

    return scaled_df

def make_A_matrix(case, def_A=A):
    A = def_A.copy()

    if "case" == "f":
        A[0, 2] = 0.
        A[1, 2] = -1.5

        return A

    elif "case" == "s":
        A[0, 2] = -.1
        A[1, 2] = 0.

        return A

    elif "case" == "t":
        A[0, 2] = 0.
        A[1, 0] = 0.
        A[1, 2] = 0.

        return A

    elif "cholesky":
        A[0, 1] = 0.
        A[0, 2] = 0.
        A[1, 2] = 0.

        return A
    
    else:
        raise ValueError("Case not recognized")


if __name__ == "__main__":
    df = read_data("data/bp.xls")
    scaled_df = parse_data(df)

    for case in ["f", "s", "t", "cholesky"]:

        A_restr = make_A_matrix(case)

        print(f"{case}: A = {A_restr}")

        results = svar(
            scaled_df, A=A_restr, B=B, trend="ctt")


        plot_var(results, var="G", folder=f"matrix_A_{case}", fevd=False)
