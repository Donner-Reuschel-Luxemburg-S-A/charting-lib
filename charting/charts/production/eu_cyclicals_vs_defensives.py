import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main(**kwargs):
    blp = BloombergSource()

    start_date = "20050101"

    df14, t14 = blp.get_series(series_id='SXAP Index', observation_start=start_date)
    df15, t15 = blp.get_series(series_id='SX86P Index', observation_start=start_date)
    df16, t16 = blp.get_series(series_id='SXNP Index', observation_start=start_date)
    df17, t17 = blp.get_series(series_id='SX6P Index', observation_start=start_date)

    title = "STOXX 600: Cyclicals vs. Defensives"
    metadata = Metadata(title=title, region=Region.DE, category=Category.SURVEY)

    chart = Chart(title=title, metadata=metadata, filename="eu_inside_stocks.jpeg")

    chart.configure_y_axis(y_axis_index=0, label="INDEX")

    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter)

    s1 = df14['y'] / df17['y']
    s3 = df16['y'] / df17['y']

    chart.add_series(x=df14.index, y=s1, label="Autos / Utilities")
    chart.add_series(x=df16.index, y=s3, label="Industrials / Utilities")

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()