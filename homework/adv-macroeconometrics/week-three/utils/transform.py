import pandas as pd

def make_lagged_data(data, variable, var_name = None):
    
    if var_name is None:
        var_name = f"lag_1_{variable}"
    
    days = data.index.get_level_values("date")
    first_day = days[0]
    second_day = days[1]
    
    lagged_data = data.loc[variable].iloc[:-1].to_numpy()

    lagged_df = data.loc[variable].copy()
    lagged_df.loc[second_day:] = lagged_data
    
    lagged_df.index = pd.MultiIndex.from_product(
        [[f"{var_name}"], lagged_df.index], names=['variable', 'date'])
    

    data_with_lag = data.append(lagged_df)
    data_with_lag = data_with_lag.drop(first_day, level="date")
    
    return data_with_lag

def make_multi_lagged(data, variables, lags = 1):
    
    lagged_var_names = []

    if isinstance(variables, str):
        variables = [variables]

    for null_var in variables:
        variable_to_lag = null_var
        
        for l in range(lags):
            var_name = f"lag_{l+1}_{null_var}"
            data = make_lagged_data(data, variable_to_lag, var_name=var_name)
            
            variable_to_lag = var_name
            
            lagged_var_names.append(var_name)
        
    return data, lagged_var_names
        