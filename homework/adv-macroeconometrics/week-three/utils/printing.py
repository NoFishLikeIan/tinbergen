import pandas as pd

pd.options.display.float_format = lambda num: f'{num:.3f}'

def pprint(beta, standard_error, regressors, durbin_watson):
    print(f"""
\033[1mWithin regression\033[0m:  

--- β: 

{pd.Series(beta.reshape(-1,), index=regressors).to_string()}, 


--- Standard errors:

{pd.DataFrame(standard_error, index=regressors, columns=regressors)}

--- DW-statistics:

d = {durbin_watson:.4f}

        """)