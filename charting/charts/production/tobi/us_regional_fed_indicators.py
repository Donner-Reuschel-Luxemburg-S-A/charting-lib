import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart


def main():
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19980101"

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

    title = "US Philadelphia Fed Indicators"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_philly.png", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="")

    chart.add_series(philly_business_outlook_df.index, philly_business_outlook_df['y'],
                     label=philly_business_outlook_title)
    chart.add_series(philly_nonmanu_df.index, philly_nonmanu_df['y'], label=philly_nonmanu_title)
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Dallas Fed Indicators"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_dallas.png", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    chart.add_series(dallas_manu_df.index, dallas_manu_df['y'], label=dallas_manu_title)
    chart.add_series(dallas_serv_df.index, dallas_serv_df['y'], label=dallas_serv_title)
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Kansas Fed Indicators"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_kansas.png", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    chart.add_series(kansas_manu_df.index, kansas_manu_df['y'], label=kansas_manu_title)
    chart.add_series(kansas_serv_df.index, kansas_serv_df['y'], label=kansas_serv_title)
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Richmond Fed Indicators"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_richmond.png", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    chart.add_series(richmond_business_outlook_df.index, richmond_business_outlook_df['y'],
                     label=richmond_business_outlook_title)
    chart.add_series(richmond_manu_df.index, richmond_manu_df['y'], label=richmond_manu_title)
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Empire Manufacturing Index"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_empire.png", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    chart.add_series(empire_df.index, empire_df['y'], label=empire_title)
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "US NY Fed Business Activity Index"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="nyfed_serv.png", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    chart.add_series(nyfed_serv_df.index, nyfed_serv_df['y'], label=nyfed_serv_title)
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
