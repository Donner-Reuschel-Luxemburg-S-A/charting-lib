import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata

DEFAULT_START_DATE = datetime.date(2017, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    d1, t1 = blp.get_series(series_id='XAG Curncy', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))

    title = "Silver"
    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.COMMODITY)
    chart = Chart(title="Silver", metadata=metadata, filename='global_silver', language=kwargs.get('language', 'en'))

    chart.configure_y_axis(y_axis_index=0, label="USD $")
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=d1.index, y=d1['y'], label=t1)
    chart.legend()
    chart.add_last_value_badge(decimals=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
