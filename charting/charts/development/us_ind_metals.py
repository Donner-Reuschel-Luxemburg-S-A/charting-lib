import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart


def main():
    blp = BloombergSource()
    fred = FredSource()

    start_time = "20230101"

    ng_df, ng_title = blp.get_series(series_id="NG1 Comdty", observation_start=start_time)
    intm_df, intm_title = blp.get_series(series_id="BCOMINSP Index", observation_start=start_time)
    #xau_df, xau_title = blp.get_series(series_id="XAU Curncy", observation_start=start_time)
    #cpi_df, cpi_title = blp.get_series(series_id="CPURNSA Index", observation_start=start_time)

    #us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)


    title = "Industriemetalle: Preisentwicklung"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_ind_metals.png", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.MonthLocator(1), major_locator=mdates.MonthLocator(2))
    chart.configure_y_axis(y_lim=[200,350],minor_locator=MultipleLocator(10), major_locator=MultipleLocator(50),label="")


    chart.add_series(intm_df.index, intm_df['y'], "Index")

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "Gas: Preisentwicklung"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_ng.png", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.MonthLocator(1), major_locator=mdates.MonthLocator(2))
    chart.configure_y_axis(y_lim=[1.5,4],minor_locator=MultipleLocator(0.5), major_locator=MultipleLocator(1),label="")


    chart.add_series(ng_df.index, ng_df['y'], "Preis")

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()



if __name__ == '__main__':
    main()
