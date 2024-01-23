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

    ip_df, ip_title = blp.get_series(series_id="IP  CHNG Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    title = "US Industrial Production 6M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.ECONOMY)

    chart = Chart(title=title, filename="us_industrial_production_mom_6.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="Percentage Points")

    chart.add_series(ip_df.index, ip_df['y'] * 12, label=ip_title, transformer=[Avg(offset=DateOffset(months=6))])

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Industrial Production 12M Ann."
    metadata = Metadata(title=title, region=Region.US, category=Category.ECONOMY)

    chart = Chart(title=title, filename="us_industrial_production_mom_12.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="Percentage Points")

    chart.add_series(ip_df.index, ip_df['y'] * 12, label=ip_title,
                     transformer=[Avg(offset=DateOffset(months=12))])

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Industrial Production YoY"
    metadata = Metadata(title=title, region=Region.US, category=Category.ECONOMY)

    chart = Chart(title=title, filename="us_industrial_production_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="Percentage Points")

    ip_df['z'] = ip_df['y'].rolling(12).sum()

    chart.add_series(ip_df.index, ip_df['z'], label=ip_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
