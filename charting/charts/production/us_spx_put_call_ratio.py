import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main():
    blp = BloombergSource()

    df1, t1 = blp.get_series(series_id='SPX Index', observation_start="20180101")
    df2, t2 = blp.get_series(series_id='PCUSEQTR Index', observation_start="20180101")

    title = "S&P 500 & Put Call Ratio"

    metadata = Metadata(title=title, region=Region.US, category=Category.EQUITY)
    chart = Chart(title=title, filename="us_spx_put_call_ratio.py.png", metadata=metadata, num_rows=2)

    chart.configure_y_axis(row_index=0, y_axis_index=0, label="USD $")
    chart.configure_y_axis(row_index=1, y_axis_index=0, label="Ratio")

    minor_locator = mdates.MonthLocator(interval=1)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1, row_index=0, y_axis_index=0)
    chart.add_series(x=df2.index, y=df2['y'], label=t2, row_index=1, y_axis_index=0)

    chart.legend()
    chart.plot()


if __name__ == '__main__':
    main()
