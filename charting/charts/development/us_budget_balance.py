import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main():
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19900101"

    tb_df, tb_title = blp.get_series(series_id="FDDSSD   Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    title = "US Budget Balance MoM"
    metadata = Metadata(title=title, region=Region.US, category=Category.ECONOMY)

    chart = Chart(title=title, filename="us_budget_balance_mom.png", metadata=metadata)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(10), major_locator=MultipleLocator(100), label="USD (bn.)")

    chart.add_series(tb_df.index, tb_df['y'], label=tb_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Budget Balance YoY"
    metadata = Metadata(title=title, region=Region.US, category=Category.CONSUMER)

    chart = Chart(title=title, filename="us_budget_balance_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(50), major_locator=MultipleLocator(200), label="Percentage Points")

    tb_df['z'] = tb_df['y'].rolling(12).sum()

    chart.add_series(tb_df.index, tb_df['z'], label=tb_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)
    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
