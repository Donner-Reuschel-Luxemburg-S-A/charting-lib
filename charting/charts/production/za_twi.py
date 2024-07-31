import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(2017, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    df, t = blp.get_series(series_id='TWI SASP Index', observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))

    title = "ZAR Trade Weighted Index Spot"

    metadata = Metadata(title=title, region=Region.ZA, category=Category.FX)

    chart = Chart(title=title, metadata=metadata, filename="za_twi.jpeg")

    chart.configure_y_axis(label="INDEX")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=df.index, y=df['y'], label=t)
    chart.add_last_value_badge(decimals=2)

    chart.legend()
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
