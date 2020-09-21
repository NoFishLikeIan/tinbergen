from utils import plotting, transform, ingest
from forecast import stats

cols = ["HOUST", "PERMIT"]
regions = ["NE", "MW", "S", "W"]

regional_hst = [f"HOUST{r}" for r in regions]

plot = False

if __name__ == '__main__':

    raw_df = ingest.import_fred()

    parsed_df = transform.standard(raw_df)

    houst_reg = parsed_df[regional_hst]

    cov, var_names = stats.sample_covariance(houst_reg)

    plotting.plot_covariance(cov, var_names, save_data=True, name="regional-cov")

    # -----------------

    if plot:
        plotting.plot_subdf(parsed_df, cols, figname="national", mul_axis=True)
        plotting.plot_subdf(parsed_df, regional_hst, figname="regional-houst", mul_axis=False)
