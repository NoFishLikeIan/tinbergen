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
    unscaled_df = df[target_cols]
    scaled_df = unscaled_df.copy()

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

    unscaled_df = unscaled_df.rename(
        columns = {
            "GCN": "G",
            "TAX": "T",
            "GDP": "Y"
        }
    )
    return scaled_df, unscaled_df

def make_A_matrix(case, def_A):
    A = def_A.copy()

    if case == "f":
        A[0, 2] = 0.
        A[1, 2] = -1.5

        return A

    elif case == "s":
        A[0, 2] = -.1
        A[1, 2] = 0.

        return A

    elif case == "t":
        A[0, 2] = 0.
        A[1, 0] = 0.
        A[1, 2] = 0.

        return A

    elif case == "cholesky":
        A[0, 1] = 0.
        A[0, 2] = 0.
        A[1, 2] = 0.

        return A
    
    else:
        raise ValueError("Case not recognized")


def get_elast(results):
    A = results.A
    elast = -A[2, 0]
    
    return elast

def G_Y_multiplier(df, unscaled_df,  brk = "1979Q3"):
    def_A = make_A_matrix("cholesky", A)
    pre = df[:brk]
    post = df[brk:]

    var_pre = svar(pre, A=def_A, B=B, trend="ctt")
    var_post = svar(post, A=def_A, B=B, trend="ctt")

    pre_mean = np.mean(unscaled_df[:brk]["Y"] / unscaled_df[:brk]["G"])
    pre_elas = get_elast(var_pre) * pre_mean

    post_mean = np.mean(unscaled_df[brk:]["Y"] / unscaled_df[brk:]["G"])
    post_elas = get_elast(var_post) * post_mean


    return pre_elas, post_elas

def pmatrix(a):
    """Returns a LaTeX pmatrix

    :a: numpy array
    :returns: LaTeX pmatrix as a string
    """
    if len(a.shape) > 2:
        raise ValueError('pmatrix can at most display two dimensions')
    lines = str(a).replace('[', '').replace(']', '').splitlines()
    rv = [r'\begin{pmatrix}']
    rv += ['  ' + ' & '.join(l.split()) + r'\\' for l in lines]
    rv +=  [r'\end{pmatrix}']
    return '\n'.join(rv)


if __name__ == "__main__":
    df = read_data("data/bp.xls")
    scaled_df, unscaled_df = parse_data(df)

    pre_elas, post_elas = G_Y_multiplier(scaled_df, unscaled_df)

    print(f"Multiplier: {pre_elas} (pre) and {post_elas} (post)")

    dummy_df = scaled_df.copy()
    dummy_df["D"] = 0.
    dummy_df["D"]["1975Q2"] = 1.

    standard_res = var(dummy_df, lags = 4)
    plot_var(standard_res, impulse = "G", response=dummy_df.columns, folder="bp/base", autocorr=True)
    

    cases =  ["f", "s", "t", "cholesky"]
    for case in cases:

        A_restr = make_A_matrix(case, A)

        print(f"Case {case}")
        results = svar(scaled_df, A=A_restr, B=B, trend="ctt", maxiter=5_000, verbose=True)
        plot_var(results, impulse="G", folder=f"bp/A-{case}", fevd=False, plot_stderr=True)

        np.savetxt(f"plots/bp/A-{case}/A-matrix.txt", results.A)

        with open(f"plots/bp/A-{case}/A-matrix.txt", "w") as file:
            string = pmatrix(results.A)
            file.write(string)
