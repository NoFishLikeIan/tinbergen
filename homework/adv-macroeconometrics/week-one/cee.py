from utils.read_data import read_data
from utils.plot import plot_var
from utils.var import var, select_lr


if __name__ == "__main__":
    df = read_data("data/cee.xls", f = "1963Q3")

    lag = select_lr(df, maxlags = 15)
    print("LR ratio: ", lag)

    standard_res = var(df, lags = 4)
    plot_var(standard_res, impulse = "FF", response=df.columns, folder="cee/ex", autocorr=True)

    ic = "bic"
    standard_res = var(df, trend="c",lags=2)
    plot_var(standard_res, impulse = "FF", folder=f"cee/{ic}")

    new_order = ["Y", "P", "PCOM", "FF", "TR", "NBR", "M1"]
    reindexed = df.reindex(columns=new_order)
    standard_res = var(reindexed, lags = 4)
    plot_var(standard_res, impulse = "FF", response=df.columns, folder="cee/swapped", autocorr=True)