from utils import plotting, transform, ingest
from forecast import stats

cols = ["HOUST", "PERMIT"]
regions = ["NE", "MW", "S", "W"]

regional_hst = [f"HOUST{r}" for r in regions]

plot = True

if __name__ == '__main__':

    raw_df = ingest.import_fred()

    parsed_df = transform.standard(raw_df)

    houst_reg = parsed_df[regional_hst]

    # -----------------

    if plot:
        plotting.plot_subdf(parsed_df, cols, figname="national", mul_axis=False)
        plotting.plot_subdf(parsed_df, regional_hst, figname="regional-houst", mul_axis=False)

        cov, var_names = stats.sample_covariance(houst_reg)
        plotting.plot_covariance(cov, var_names, save_data=True, name="regional-cov", annot=True)


        plotting.plot_acf(houst_reg, figname="regional-acf")
