import os
import pandas as pd

from typing import Iterable, Tuple, NewType

Codes = NewType("Codes", Iterable[Tuple[str, str]])

def construct_series(core: pd.DataFrame, country_codes: Codes):
    variables = core.loc[:, "S/Y":].columns.tolist()
    years = pd.to_datetime(core[core["Country"] == 1]["Year"], format="%Y")

    frames = []
    
    for var in variables:
        var_df = pd.DataFrame(index=years)
        
        for code, country in country_codes:

            series = core[core["Country"] == code][var]
            series.index = years

            var_df[country] = series
        
        frames.append(var_df)

    df = pd.concat(frames, axis=0, keys=variables)

    df.index.set_names(["variable", "date"], inplace = True)

    return df

        

def extract_country_codes(meta_data: pd.DataFrame) -> Codes:
    countries = 19
    
    f_code, f_country = meta_data.columns.tolist()[1:]    
        
    codes = [f_code, *meta_data[f_code][:countries-1].tolist()]
    countries = [f_country, *meta_data[f_country][:countries-1].tolist()]
    
    return list(zip(codes, countries))

def read_data(data_path: str) -> pd.DataFrame:
    if not os.path.isfile(data_path):
        raise FileNotFoundError(f"Provided path ({data_path}")

    raw = pd.read_excel(data_path)
    
    core_data = raw.loc[:, :"SG/Y"]
    meta_data = raw.loc[:, "Countries":]
    
    country_codes = extract_country_codes(meta_data)

    df = construct_series(core_data, country_codes)     

    return df


if __name__ == '__main__':
    read_data("data/hw3.xls")