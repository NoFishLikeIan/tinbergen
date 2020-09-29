import os
import pandas as pd

from utils import plotting, transform, ingest
from forecast import stats, rf, run

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

cols = ["HOUST", "PERMIT"]
regions = ["NE", "MW", "S", "W"]

regional_hst = [f"HOUST{r}" for r in regions]
regional_permits = [f"PERMIT{r}" for r in regions]

plot = False
cached_model_path = "data/cache_model.sav"

init_year = "1960-01-01"
end_train = "2008-12-01"

lags = 12

if __name__ == '__main__':

    if os.path.isfile("data/sample.csv"):

        df = pd.read_csv("data/sample.csv").rename(columns = {"Unnamed: 0": "date"}).set_index("date")
        df.index = pd.to_datetime(df.index)

    else:
        raw_df = ingest.import_fred()

        parsed_df = transform.standard(raw_df)

        national_houst = parsed_df["HOUST"]

        houst_reg = parsed_df[regional_hst]
        permits_reg = parsed_df[regional_permits]


        train = houst_reg[init_year:end_train]
        exog = permits_reg[init_year:end_train]

        test = houst_reg[end_train:]

        forecaster = rf.make_forecaster(train, lags=lags, exog_df=exog, verbose = 0)



        df = run.iterative_forecast(
            forecaster, train,
            lags=lags, exog=permits_reg, periods=12, against_baseline=True
        )

        df.to_csv("data/sample.csv", index=True)
    
    

    # -----------------

    if plot:
        plotting.plot_subdf(parsed_df, cols, figname="national", mul_axis=False)
        plotting.plot_subdf(parsed_df, regional_hst, figname="regional-houst", mul_axis=False)

        cov, var_names = stats.sample_covariance(houst_reg)
        plotting.plot_covariance(cov, var_names, save_data=True, name="regional-cov", annot=True)


        plotting.plot_acf(houst_reg, figname="regional-acf")

        plotting.plot_density(houst_reg, stats.spectral_density, figname="regional-spectr", save=True)

        
