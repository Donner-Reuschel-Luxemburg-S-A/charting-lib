import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main(**kwargs):
    blp = BloombergSource()

    start_date = "20050101"

    df7, t7 = blp.get_series(series_id='GRZEEUCU Index', observation_start=start_date)
    df8, t8 = blp.get_series(series_id='GRZEEUEX Index', observation_start=start_date)

    title = "ZEW Eurozone Surveys"
    metadata = Metadata(title=title, region=Region.EU, category=Category.SURVEY)

    chart = Chart(title=title, metadata=metadata, filename="eu_zew_business_climate.png")

    chart.configure_y_axis(y_axis_index=0, label="Index")

    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter)

    chart.add_series(x=df7.index, y=df7['y'], label=t7)
    chart.add_series(x=df8.index, y=df8['y'], label=t8)

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()