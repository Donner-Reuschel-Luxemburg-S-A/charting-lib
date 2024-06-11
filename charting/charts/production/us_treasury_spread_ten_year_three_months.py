import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main(**kwargs):
    blp = BloombergSource()
    df1, t1 = blp.get_series(series_id='USYC3M10 Index', observation_start="20220131")

    title = "10 Year - 3 Month Treasury Yield Spread"
    metadata = Metadata(title=title, region=Region.US, category=Category.RATES)
    chart = Chart(title=title, metadata=metadata, filename="us_3m10y_curve.png")

    chart.configure_y_axis(y_axis_index=0, label="BPS", minor_locator=MultipleLocator(20),
                           major_locator=MultipleLocator(40))

    minor_locator = mdates.MonthLocator(interval=1)
    major_locator = mdates.MonthLocator(interval=4)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=title)
    chart.add_horizontal_line()

    chart.legend()
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
