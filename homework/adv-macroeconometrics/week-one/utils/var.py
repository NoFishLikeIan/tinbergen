import numpy as np

from statsmodels.tsa.vector_ar import var_model, svar_model
from scipy.stats.distributions import chi2

def var(df, lags = -1, **kwargs):

    model = var_model.VAR(df, dates=df.index, freq="Q")

    if lags > 0:
        print(f"Using given lag order ({lags})...")
        results = model.fit(lags, verbose=True, **kwargs)
        
    else:
        print("Finding optimum lag order...")
        results = model.fit(verbose=True, **kwargs) 

    return results

def svar(df, A = None, B = None, **kwargs):

    model = svar_model.SVAR(
        df,
        dates=df.index, 
        A=A, B=B, svar_type="AB"
    )

    results = model.fit(maxlags=4, **kwargs) 

    return results

def make_lag_iter(maxlags):
    return list(zip(
            range(1, maxlags + 1),
            range(0, maxlags)
        ))[::-1]

def lr_test(l1, l2, df_resid):
    lr = df_resid*(l1 - l2)
    p = chi2.sf(lr, 1)

    return p < .05

def select_lr(df, maxlags = 15, **kwargs):

    lag_list = make_lag_iter(maxlags)

    model = var_model.VAR(df, dates=df.index, freq="Q")

    for more_l, less_l in lag_list:
        big_model = model.fit(more_l, **kwargs)
        small_model = model.fit(less_l, **kwargs)

        reject = lr_test(big_model.llf, small_model.llf, big_model.df_resid)

        if reject:
            return more_l

    else:
        raise ValueError("Never rejected, increase maxlags")
        