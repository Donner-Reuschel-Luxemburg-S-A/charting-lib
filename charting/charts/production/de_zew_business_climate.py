import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main(**kwargs):
    blp = BloombergSource()

    start_date = "20050101"

    df4, t4 = blp.get_series(series_id='GRZECURR Index', observation_start=start_date)
    df5, t5 = blp.get_series(series_id='GRZEWI Index', observation_start=start_date)

    title = "ZEW Germany Surveys"
    metadata = Metadata(title=title, region=Region.DE, category=Category.SURVEY)

    chart = Chart(title=title, metadata=metadata, filename="de_zew_business_climate", language=kwargs.get('language', 'en'))

    chart.configure_y_axis(y_axis_index=0, label="INDEX")

    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter)

    chart.add_series(x=df4.index, y=df4['y'], label=t4)
    chart.add_series(x=df5.index, y=df5['y'], label=t5)
    chart.add_last_value_badge(decimals=2)

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')