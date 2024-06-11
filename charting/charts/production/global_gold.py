import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata


def main(**kwargs):
    blp = BloombergSource()
    d1, t1 = blp.get_series(series_id='XAU Curncy', observation_start="20170101")

    title = "Gold"
    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.COMMODITY)
    chart = Chart(title="Gold", metadata=metadata, filename='global_gold.png')

    chart.configure_y_axis(y_axis_index=0, label="USD", minor_locator=MultipleLocator(100),
                           major_locator=MultipleLocator(200))

    major_locator = mdates.MonthLocator(interval=12)
    minor_locator = mdates.MonthLocator(interval=3)

    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label=t1)
    chart.legend()
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
