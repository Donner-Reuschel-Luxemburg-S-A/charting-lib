import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main(**kwargs):
    blp = BloombergSource()
    df1, t1 = blp.get_series(series_id='DEYC1030 Index', observation_start="20200101")

    title = "Germany Government Bonds Spread 30-10-Year"
    metadata = Metadata(title=title, region=Region.DE, category=Category.RATES)
    chart = Chart(title=title, metadata=metadata, filename="de_gov_spread_30y_10y.png")

    chart.configure_y_axis(y_axis_index=0, label="BPS", minor_locator=MultipleLocator(5),
                           major_locator=MultipleLocator(10))

    minor_locator = mdates.MonthLocator(interval=1)
    major_locator = mdates.MonthLocator(interval=6)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_horizontal_line()
    chart.add_series(x=df1.index, y=df1['y'], label=title)

    chart.legend()
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
