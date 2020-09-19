from utils import plotting, transform, ingest

cols = ["HOUST", "PERMIT"]
regions = ["NE", "MW", "S", "W"]

regional_hst = [f"HOUST{r}" for r in regions]

if __name__ == '__main__':

    raw_df = ingest.import_fred()

    parsed_df = transform.standard(raw_df)

    plotting.plot_subdf(parsed_df, cols, figname="national", mul_axis=True)
    plotting.plot_subdf(parsed_df, regional_hst, figname="regional-houst", mul_axis=False)
