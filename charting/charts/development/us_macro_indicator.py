import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart


def main():
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19600101"

    philly_business_outlook_df, philly_business_outlook_title = blp.get_series(series_id="OUTFGAF Index", observation_start=start_time)
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

    credit_impulse_df, credit_impulse_title = blp.get_series(series_id="BCMPCIUS Index", observation_start=start_time)

    ff_df, ff_title = blp.get_series(series_id="FDTR Index", observation_start=start_time)

    df_macro_ind = philly_business_outlook_df
    df_macro_ind['y'] = (philly_business_outlook_df['y']<0).astype(int)*(ism_manu_df['y']<50).astype(int)*(credit_impulse_df['y']<0).astype(int)




    title = "US Macro Index (ISM Manufacturing, Philly Fed Business Outlook, Credit Impuls)"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="macro_index_ff_rate.png", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5),label="")

    chart.add_series(ff_df.index, ff_df['y'], label=ff_title)
    #chart.add_series(df_macro_ind.index, df_macro_ind['y'], label="Indicator")
    chart.add_vertical_line(x=df_macro_ind.index, y=df_macro_ind["y"])

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
