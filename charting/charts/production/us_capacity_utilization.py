import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main():
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19290101"

    cap_df, cap_title = blp.get_series(series_id="CPTICHNG Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    title = "US Capacity Utilization"
    metadata = Metadata(title=title, region=Region.US, category=Category.ECONOMY)

    chart = Chart(title=title, filename="us_capacity_utilization.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="Percentage Points")

    chart.add_series(cap_df.index, cap_df['y'], label=cap_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.legend(ncol=1)
    chart.plot()


if __name__ == '__main__':
    main()
