import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata
from charting.transformer.ytd import Ytd

DEFAULT_START_DATE = datetime.date(2024, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    df1, t1 = blp.get_series(series_id='LBEATREU Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df2, t2 = blp.get_series(series_id='LEU1TREU Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))

    title = "European Interest Rate Markets"
    metadata = Metadata(title=title, region=Region.EU, category=Category.RATES)

    chart = Chart(title=title, metadata=metadata, filename="eu_rates_performance", language=kwargs.get('language', 'en'))

    chart.configure_y_axis(label="PERCENTAGE POINTS")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=df1.index, y=df1['y'], label="Euro Aggregate Index", transformer=Ytd())
    chart.add_series(x=df2.index, y=df2['y'], label="Euro Aggregate 1-10 Index", transformer=Ytd())
    chart.add_last_value_badge(decimals=2)
    chart.add_horizontal_line()

    chart.legend(ncol=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
