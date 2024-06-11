import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main(**kwargs):
    blp = BloombergSource()
    d1, t1 = blp.get_series(series_id='TWTREXPY Index', observation_start="19900101")

    title = "Taiwan - Total Export Trade (YoY)"
    metadata = Metadata(title=title, region=Region.TW, category=Category.ECONOMY)
    chart = Chart(title=title, metadata=metadata, filename="tw_export_yoy.png")

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", minor_locator=MultipleLocator(5),
                           major_locator=MultipleLocator(10))

    minor_locator = mdates.YearLocator(base=1)
    major_locator = mdates.YearLocator(base=5)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label=title)
    chart.add_horizontal_line(y=d1['y'].iloc[-1])
    chart.add_last_value_badge()

    chart.legend()
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
