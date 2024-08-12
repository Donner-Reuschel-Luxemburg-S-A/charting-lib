import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata

DEFAULT_START_DATE = datetime.date(2000, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    fed, _ = blp.get_series(series_id='CERBTTAL Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    ecb, _ = blp.get_series(series_id='EBBSTOTA Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    boj, _ = blp.get_series(series_id='BJACTOTL Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))

    fed['y'] = (fed['y'] / fed['y'].iloc[0]) * 100
    ecb['y'] = (ecb['y'] / ecb['y'].iloc[0]) * 100
    boj['y'] = (boj['y'] / boj['y'].iloc[0]) * 100

    title = "Total Assets - Central Banks"
    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.CB)

    chart = Chart(title=title, metadata=metadata, filename="global_central_banks", language=kwargs.get('language', 'en'))

    chart.configure_y_axis(label="INDEX")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=fed.index, y=fed['y'], label="Federal Reserve (FED)")
    chart.add_series(x=ecb.index, y=ecb['y'], label="European Central Bank (ECB)")
    chart.add_series(x=boj.index, y=boj['y'], label="Bank of Japan (BOJ)")

    chart.legend(ncol=3)
    chart.add_last_value_badge(decimals=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
