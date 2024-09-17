import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata

DEFAULT_START_DATE = datetime.date(2020, 9, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    df1, t1 = blp.get_series(series_id='ECMAM2YY Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df2, t2 = blp.get_series(series_id='TWI EUSP Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))

    title = "M2 Money supply growth and EUR performance"
    metadata = Metadata(title=title, region=Region.EU, category=Category.CB)

    chart = Chart(title=title, num_y_axis=2, metadata=metadata, filename="m2_twi_eur", language=kwargs.get('language', 'en'))

    chart.configure_y_axis(y_axis_index=0, label="PERCENTAGE POINTS")
    chart.configure_y_axis(y_axis_index=1, label="INDEX")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=df1.index, y=df1['y'], label=t1, y_axis_index=0)
    chart.add_series(x=df2.index, y=df2['y'], label=t2, y_axis_index=1)

    chart.legend(ncol=2)
    chart.add_horizontal_line(y_axis_index=0)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
