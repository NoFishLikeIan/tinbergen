import numpy as np

from statsmodels.tsa.vector_ar import var_model, svar_model

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

    print("Finding optimum lag order...")
    results = model.fit(**kwargs) 

    return results