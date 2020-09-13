import numpy as np
import pandas as pd

from utils.read_data import read_data
from utils.plot import plot_var
from utils.var import var

transform = ["RGDP", "RGOV", "RCONS", "RINV"]
to = ["Y", "G", "CONS", "INV"]

name_map = dict(zip(transform, to))

def parse_data(df: pd.DataFrame)->pd.DataFrame:

    new_df = df.copy()
    pop = new_df["POP"]
    
    for transf_var in transform:
        trans_data = np.log(new_df[transf_var] / pop)
        new_df[name_map[transf_var]] = trans_data

    return new_df.drop(transform, axis = 1)
    

if __name__ == "__main__":
    df = read_data("data/ramey.xls")
    parsed_df = parse_data(df)["1960Q1":]

    restr_var = ["G", "T", "Y"]
    restr_df = parsed_df[restr_var]
    res = var(restr_df, trend="ctt", lags = 4)
    plot_var(res, impulse="G", folder="ramey/base")

    aug_var = restr_var + ["CONS", "INV"]
    aug_df = parsed_df[aug_var]
    res = var(aug_df, trend="ctt", lags = 4)
    plot_var(res, impulse="G", folder="ramey/aug")

    war_var = ["WAR"] + aug_var 
    war_df = parsed_df[war_var]
    res = var(war_df, trend="ctt", lags = 4)
    plot_var(res, impulse="WAR", folder="ramey/war")


    mil_var = ["MIL"] + aug_var 
    mil_df = parsed_df[mil_var]
    res = var(mil_df, trend="ctt", lags = 4)
    plot_var(res, impulse="MIL", folder="ramey/mil")

    
    
