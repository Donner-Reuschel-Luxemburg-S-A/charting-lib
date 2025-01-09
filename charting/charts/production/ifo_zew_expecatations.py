import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(2018, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    d1, t1 = blp.get_series(series_id='GRZEWI Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    d2, t2 = blp.get_series(series_id='GRIFPEX Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))

    title = "IFO vs. ZEW Expectations"
    metadata = Metadata(title=title, region=Region.DE, category=Category.SURVEY)
    chart = Chart(title=title, metadata=metadata, filename="ifo_zew_expectations", num_y_axis=2, language=kwargs.get('language', 'en'))

    chart.configure_y_axis(y_axis_index=0, label="Points", y_lim=(70, 120))
    chart.configure_y_axis(y_axis_index=1, label="Points", y_lim=(-80, 90))

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=d2.index, y=d2['y'], label="IFO Pan Germany Business Expectations",
                     y_axis_index=0)
    chart.add_series(x=d1.index, y=d1['y'], label="ZEW Germany Expectations of Economic Growth",
                     y_axis_index=1)

    chart.add_horizontal_line()
    chart.add_last_value_badge(decimals=2)
    chart.legend()

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
