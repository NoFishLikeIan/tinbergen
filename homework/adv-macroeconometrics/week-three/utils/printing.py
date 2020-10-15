import pandas as pd

pd.options.display.float_format = lambda num: f'{num:.6f}'

def pprint(
    beta, standard_error, regressors, 
    durbin_watson = None, title = "Withing regression"
    ):

    table = f"""
\033[1m{title}\033[0m:  

--- β: 

{pd.Series(beta.reshape(-1,), index=regressors).to_string()}, 


--- Standard errors:

{pd.DataFrame(standard_error, index=regressors, columns=regressors)}
        """

    if durbin_watson is not None:
        table += f"""
--- Durbin-Watson

d = {durbin_watson:.4f}

        """

    print(table)