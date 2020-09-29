import os
import pandas as pd

def_url = "https://s3.amazonaws.com/files.fred.stlouisfed.org/fred-md/monthly/current.csv"

def import_fred(url = def_url) -> pd.DataFrame:
    cur_dir = os.getcwd()
    
    data_dir = f"{cur_dir}/data"

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    file_path = f"{data_dir}/fred_data.csv"

    if os.path.isfile(file_path):
        print(f"Using cached data at {file_path}...")

        return pd.read_csv(file_path)
    
    else:
        raw_df = pd.read_csv(url)
        raw_df.to_csv(file_path, index=False)

        return raw_df