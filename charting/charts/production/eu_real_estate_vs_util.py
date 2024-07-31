import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main(**kwargs):
    blp = BloombergSource()

    start_date = "20050101"

    df15, t15 = blp.get_series(series_id='SX86P Index', observation_start=start_date)
    df17, t17 = blp.get_series(series_id='SX6P Index', observation_start=start_date)

    title = "STOXX 600: Real Estate vs. Utes"
    metadata = Metadata(title=title, region=Region.DE, category=Category.SURVEY)

    chart = Chart(title=title, metadata=metadata, filename="eu_inside_stocks2.jpeg")

    chart.configure_y_axis(y_axis_index=0, label="INDEX")

    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter)

    s2 = df15['y'] / df17['y']

    chart.add_series(x=df15.index, y=s2, label="Real Estate / Utilities")
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()