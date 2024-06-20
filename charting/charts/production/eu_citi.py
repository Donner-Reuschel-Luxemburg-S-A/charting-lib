import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main(**kwargs):
    blp = BloombergSource()

    start_date = "20050101"

    # Citi
    df9, t9 = blp.get_series(series_id='CESIEUR Index', observation_start=start_date)

    title = "Citi Economic Surprise Index: Eurozone"
    metadata = Metadata(title=title, region=Region.DE, category=Category.SURVEY)

    chart = Chart(title=title, metadata=metadata, filename="eu_citi.png")

    chart.configure_y_axis(y_axis_index=0, label="Index")
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter)

    chart.add_series(x=df9.index, y=df9['y'], label=t9)

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()