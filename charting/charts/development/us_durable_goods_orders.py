import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from charting.transformer.avg import Avg


def main():
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19980101"

    do_df, do_title = blp.get_series(series_id="DGNOCHNG Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    title = "US Durable Goods Orders 6M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.ECONOMY)

    chart = Chart(title=title, filename="us_durable_goods_orders_mom_6.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=2))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(10), label="Percentage Points")

    chart.add_series(do_df.index, do_df['y'] * 12, label=do_title, transformer=[Avg(offset=DateOffset(months=6))])

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Durable Goods 12M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.ECONOMY)

    chart = Chart(title=title, filename="us_durable_goods_orders_mom_12.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=2))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(10), label="Percentage Points")

    chart.add_series(do_df.index, do_df['y'] * 12, label=do_title,
                     transformer=[Avg(offset=DateOffset(months=12))])

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Durable Goods Orders YoY"
    metadata = Metadata(title=title, region=Region.US, category=Category.CONSUMER)

    chart = Chart(title=title, filename="us_durable_goods_orders_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=2))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(10), label="Percentage Points")

    do_df['z'] = do_df['y'].rolling(12).sum()

    chart.add_series(do_df.index, do_df['z'], label=do_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
