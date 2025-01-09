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
    d1, t1 = blp.get_series(series_id='GRCPXEEY Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    d2, t2 = blp.get_series(series_id='GRCP20YY Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))

    title = "Germany CPI & CPI excl. Food & Energy"
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)
    chart = Chart(title=title, metadata=metadata, filename="de_cpi_corecpi", language=kwargs.get('language', 'en'))

    chart.configure_y_axis(label="PERCENTAGE POINTS")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=d2.index, y=d2['y'], label="Germany CPI")
    chart.add_series(x=d1.index, y=d1['y'], label="Germany CPI excl. Food & Energy")

    chart.add_horizontal_line()
    chart.add_last_value_badge(decimals=2)
    chart.legend(ncol=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
