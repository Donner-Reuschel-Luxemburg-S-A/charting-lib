import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart


def main(**kwargs):
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19600101"

    us10y_df, us10y_title = blp.get_series(series_id="USGG10YR Index", observation_start=start_time)
    us3m_df, us3m_title = blp.get_series(series_id="USGG3M Index", observation_start=start_time)

    yc_df = us10y_df
    yc_df['y'] = us10y_df['y'] - us3m_df['y']
    yc_title = "Yield Curve: 3M - 10Y"

    philly_business_outlook_df, philly_business_outlook_title = blp.get_series(series_id="OUTFGAF Index",
                                                                               observation_start=start_time)  # 1967
    philly_nonmanu_df, philly_nonmanu_title = blp.get_series(series_id="PNMARADI Index",
                                                             observation_start=start_time)  # 2011

    dallas_manu_df, dallas_manu_title = blp.get_series(series_id="DFEDGBA Index", observation_start=start_time)  # 2004
    dallas_serv_df, dallas_serv_title = blp.get_series(series_id="DSERGBCC Index", observation_start=start_time)  # 2007

    kansas_manu_df, kansas_manu_title = blp.get_series(series_id="KCLSSACI Index", observation_start=start_time)  # 2002
    kansas_serv_df, kansas_serv_title = blp.get_series(series_id="KCSSMCOM Index", observation_start=start_time)  # 2014

    richmond_business_outlook_df, richmond_business_outlook_title = blp.get_series(series_id="RCSSCLBC Index",
                                                                                   observation_start=start_time)  # 2011
    richmond_manu_df, richmond_manu_title = blp.get_series(series_id="RCHSINDX Index",
                                                           observation_start=start_time)  # 1994

    empire_df, empire_title = blp.get_series(series_id="EMPRGBCI Index", observation_start=start_time)  # 2002

    nyfed_serv_df, nyfed_serv_title = blp.get_series(series_id="NYBLCNBA Index", observation_start=start_time)  # 2004

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    ism_manu_df, ism_manu_title = blp.get_series(series_id="NAPMPMI Index", observation_start=start_time)  # 1967
    ism_serv_df, ism_serv_title = blp.get_series(series_id="NAPMNMI Index", observation_start=start_time)  # 1997

    chicago_pmi_df, chicago_pmi_title = blp.get_series(series_id="CHPMINDX Index", observation_start=start_time)  # 1967

    credit_impulse_df, credit_impulse_title = blp.get_series(series_id="BCMPCIUS Index", observation_start=start_time)

    ff_df, ff_title = blp.get_series(series_id="FDTR Index", observation_start=start_time)

    df_macro_ind = philly_business_outlook_df * 0
    df_macro_ind['y'] = (philly_business_outlook_df['y'] < 0).astype(int) + (ism_manu_df['y'] < 50).astype(int) + (
            yc_df['y'] < 0).astype(int) + (credit_impulse_df['y'] < 0).astype(int) + (ism_serv_df['y'] < 50).astype(
        int) + (richmond_manu_df['y'] < 0).astype(int)

    df_macro_ind_long = philly_business_outlook_df * 0
    df_macro_ind_long['y'] = (philly_business_outlook_df['y'] < 0).astype(int) + (ism_manu_df['y'] < 50).astype(int) + (
            yc_df['y'] < 0).astype(int) + (credit_impulse_df['y'] < 0).astype(int) + (
                                     chicago_pmi_df['y'] < 50).astype(int)

    title = "D&R US Recession Indicator"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="macro_index_ff_rate.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(1), label="")

    chart.add_series(ff_df.index, ff_df['y'], label=ff_title, y_axis_index=1)
    chart.add_series(df_macro_ind_long.index, df_macro_ind_long['y'].interpolate(), label="D&R Recession Indicator")

    # chart.add_series(df_macro_ind.index, df_macro_ind['y'], label="Indicator")
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label="US Recession")

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
