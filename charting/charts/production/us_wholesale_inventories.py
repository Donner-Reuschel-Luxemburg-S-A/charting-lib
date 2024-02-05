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

    start_time = "19700101"

    wholesale_inv_df, wholesale_inv_title = blp.get_series(series_id="MWINCHNG Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    title = "US Wholesale Inventories 6M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.ECONOMY)

    chart = Chart(title=title, filename="us_wholesale_inventories_mom_6.png", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="Percentage Points")

    df = wholesale_inv_df = wholesale_inv_df.iloc[6:, ]
    chart.add_series(df.index, df['y'] * 12, label=wholesale_inv_title, transformer=[Avg(offset=DateOffset(months=6))])

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Wholesale Inventories MoM"
    metadata = Metadata(title=title, region=Region.US, category=Category.ECONOMY)

    chart = Chart(title=title, filename="us_wholesale_inventories_mom.png", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(1), label="Percentage Points")

    chart.add_series(wholesale_inv_df.index, wholesale_inv_df['y'], label=wholesale_inv_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Wholesale Inventories YoY"
    metadata = Metadata(title=title, region=Region.US, category=Category.CONSUMER)

    chart = Chart(title=title, filename="us_wholesale_inventories_yoy.png", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="Percentage Points")

    wholesale_inv_df['z'] = wholesale_inv_df['y'].rolling(12).sum()
    wholesale_inv_df = wholesale_inv_df.iloc[12:, ]

    chart.add_series(wholesale_inv_df.index, wholesale_inv_df['z'], label=wholesale_inv_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
