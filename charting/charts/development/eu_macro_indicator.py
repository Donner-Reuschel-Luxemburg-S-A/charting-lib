import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart


def main():
    blp = BloombergSource()
    fred = FredSource()

    start_time = "20050101"

    de10y_df, de10y_title =  blp.get_series(series_id="GBDR10 Index", observation_start=start_time)
    de1_df, de1_title = blp.get_series(series_id="GDBR1 Index", observation_start=start_time)

    yc_df = de10y_df
    yc_df['y'] = de10y_df['y']-de1_df['y']
    yc_title = "Yield Curve: 1Y - 10Y"

    ifo_business_outlook_df, ifo_business_outlook_title = blp.get_series(series_id="GRIFPEX Index", observation_start=start_time) #1967

    gfk_consume_climate_df, gfk_consume_climate_title = blp.get_series(series_id="ECO1GFKC Index", observation_start=start_time) #1967

    zew_exp_df, zew_exp_title = blp.get_series(series_id="GRZEWI Index", observation_start=start_time)  # 1967

    credit_impulse_df, credit_impulse_title = blp.get_series(series_id="BCMPCIGD Index", observation_start=start_time)

    ecb_df, ecb_title = blp.get_series(series_id="EUORDEPO Index", observation_start=start_time)

    df_macro_ind_long = ifo_business_outlook_df * 0
    df_macro_ind_long['y'] = (ifo_business_outlook_df['y'] < 100).astype(int) + (zew_exp_df['y'] < 0).astype(int)+ (yc_df['y'] < 0).astype(int)+(credit_impulse_df['y']<0).astype(int)+(gfk_consume_climate_df['y']<0).astype(int)

    title = "D&R EU Recession Indicator"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="macro_index_eu_rate.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(1),y_axis_index=0,label="Score")
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(1),y_axis_index=1, label="ECB Deposit Rate (%)")

    chart.add_series(ecb_df.index, ecb_df['y'], label=ecb_title,y_axis_index=1)
    chart.add_series(df_macro_ind_long.index, df_macro_ind_long['y'].interpolate(),label="D&R Recession Indicator")

    #chart.add_series(df_macro_ind.index, df_macro_ind['y'], label="Indicator")
    #chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label="US Recession")


    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
