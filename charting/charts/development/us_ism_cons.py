import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart


def main(**kwargs):
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19500101"

    philly_business_outlook_df, philly_business_outlook_title = blp.get_series(series_id="OUTFGAF Index",
                                                                               observation_start=start_time)
    philly_nonmanu_df, philly_nonmanu_title = blp.get_series(series_id="PNMARADI Index", observation_start=start_time)

    dallas_manu_df, dallas_manu_title = blp.get_series(series_id="DFEDGBA Index", observation_start=start_time)
    dallas_serv_df, dallas_serv_title = blp.get_series(series_id="DSERGBCC Index", observation_start=start_time)

    kansas_manu_df, kansas_manu_title = blp.get_series(series_id="KCLSSACI Index", observation_start=start_time)
    kansas_serv_df, kansas_serv_title = blp.get_series(series_id="KCSSMCOM Index", observation_start=start_time)

    richmond_business_outlook_df, richmond_business_outlook_title = blp.get_series(series_id="RCSSCLBC Index",
                                                                                   observation_start=start_time)
    richmond_manu_df, richmond_manu_title = blp.get_series(series_id="RCHSINDX Index", observation_start=start_time)

    empire_df, empire_title = blp.get_series(series_id="EMPRGBCI Index", observation_start=start_time)

    nyfed_serv_df, nyfed_serv_title = blp.get_series(series_id="NYBLCNBA Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    ism_manu_df, ism_manu_title = blp.get_series(series_id="NAPMPMI Index", observation_start=start_time)
    ism_serv_df, ism_serv_title = blp.get_series(series_id="NAPMNMI Index", observation_start=start_time)

    nfp_df, nfp_title = blp.get_series(series_id="NFP TCH Index", observation_start=start_time)

    credit_impulse_df, credit_impulse_title = blp.get_series(series_id="BCMPCIUS Index", observation_start=start_time)

    ff_df, ff_title = blp.get_series(series_id="FDTR Index", observation_start=start_time)

    ind = ism_manu_df
    ind['y'] = ind['y'] - 50

    ind['s'] = ind.groupby(ind['y'].gt(0).astype(int).diff().ne(0).cumsum()).cumcount().add(1) * ind['y'].gt(0).replace(
        {True: 1, False: -1})
    ind['s'] = ind['s'] * (-1)
    ind['s'] = ind['s'].clip(lower=0)

    nfp_df['s'] = nfp_df['y'].rolling(3).mean()
    nfp_df[nfp_df < -1000] = -1000

    title = "US ISM Manufacturing: Consecutive Months in Contraction vs. Recessions"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_ism_cons_rec.jpeg", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="")

    chart.add_series(ind.index, ind['s'], label="Consecutive Months in Contraction")
    # chart.add_series(nfp_df.index, nfp_df['s'], label="Cumulative NFPs",y_axis_index=1)
    # chart.add_series(df_macro_ind.index, df_macro_ind['y'], label="Indicator")
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"])

    chart.add_horizontal_line(y=0, y_axis_index=1)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
