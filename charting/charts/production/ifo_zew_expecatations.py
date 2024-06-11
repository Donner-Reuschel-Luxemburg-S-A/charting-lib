import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main(**kwargs):
    blp = BloombergSource()
    d1, t1 = blp.get_series(series_id='GRZEWI Index', observation_start='20180101')
    d2, t2 = blp.get_series(series_id='GRIFPEX Index', observation_start='20180101')

    title = "IFO vs. ZEW Expectations"
    metadata = Metadata(title=title, region=Region.DE, category=Category.SURVEY)
    chart = Chart(title=title, metadata=metadata, filename="ifo_zew_expectations.png", num_y_axis=2)

    chart.configure_y_axis(y_axis_index=0, label="Points", y_lim=(70, 120), minor_locator=MultipleLocator(5),
                           major_locator=MultipleLocator(10))
    chart.configure_y_axis(y_axis_index=1, label="Points", y_lim=(-80, 90), minor_locator=MultipleLocator(10),
                           major_locator=MultipleLocator(20))

    minor_locator = mdates.MonthLocator(interval=6)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d2.index, y=d2['y'], label="IFO Pan Germany Business Expectations",
                     y_axis_index=0)
    chart.add_series(x=d1.index, y=d1['y'], label="ZEW Germany Expectations of Economic Growth",
                     y_axis_index=1)

    # chart.add_horizontal_line()
    # chart.add_last_value_badge()
    chart.legend(ncol=1)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
