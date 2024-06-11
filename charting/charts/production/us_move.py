import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main(**kwargs):
    blp = BloombergSource()
    d1, t1 = blp.get_series(series_id='MOVE Index', observation_start="20220101")

    title = "Implied Volatility U.S. Treasury"
    metadata = Metadata(title=title, region=Region.US, category=Category.VOLATILITY)
    chart = Chart(title=title, metadata=metadata, filename="us_move_index.png")

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", y_lim=(50, 210))

    major_locator = mdates.MonthLocator(interval=3)
    minor_locator = mdates.MonthLocator(interval=1)

    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label=t1)

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
