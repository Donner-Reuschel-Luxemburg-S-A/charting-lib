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
    d1, t1 = blp.get_series(series_id='XAU Curncy', observation_start=observation_start.strftime('%Y%m%d'),
                            observation_end=observation_end.strftime('%Y%m%d'))
    d2, t2 = blp.get_series(series_id='XAG Curncy', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))

    title = "Gold & Silver"
    t1 = "Gold USD"
    t2 = "Silver USD"

    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.COMMODITY)
    chart = Chart(title="Gold", metadata=metadata, num_y_axis=2, filename='global_gold_silver', language=kwargs.get('language', 'en'))

    chart.configure_y_axis(label="USD $", y_axis_index=0)
    chart.configure_y_axis(label="USD $", y_axis_index=1)

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=d1.index, y=d1['y'], label=t1, y_axis_index=0)
    chart.add_series(x=d2.index, y=d2['y'], label=t2, y_axis_index=1)

    chart.legend(ncol=2)
    chart.add_last_value_badge(decimals=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
