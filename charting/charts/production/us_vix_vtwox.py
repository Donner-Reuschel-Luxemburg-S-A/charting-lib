import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main():
    blp = BloombergSource()
    fred = FredSource()

    d1, t1 = fred.get_series(series_id='VIXCLS', observation_start="2022-01-01")
    d2, t2 = blp.get_series(series_id='V2X Index', observation_start="20220101")

    title = "VIX & V2X Volatility Markets"
    metadata = Metadata(title=title, region=[Region.US, Region.EU], category=Category.VOLATILITY)
    chart = Chart(title=title, metadata=metadata, filename="us_vix_v2x.png")

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", y_lim=(10, 50))

    major_locator = mdates.MonthLocator(interval=3)
    minor_locator = mdates.MonthLocator(interval=1)

    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label="Implied Volatility S&P 500")
    chart.add_series(x=d2.index, y=d2['y'], label="Implied Volatility Eurostoxx 50")

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
