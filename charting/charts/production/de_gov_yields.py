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
    df1, t1 = blp.get_series(series_id='GDBR2 Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df2, t2 = blp.get_series(series_id='GDBR10 Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df3, t3 = blp.get_series(series_id='GDBR30 Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))

    title = "Germany Government Bonds"
    metadata = Metadata(title=title, region=Region.DE, category=Category.RATES)
    chart = Chart(title=title, metadata=metadata, filename="de_gov_yields", language=kwargs.get('language', 'en'))

    chart.configure_y_axis(label="PERCENTAGE POINTS")
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=df1.index, y=df1['y'], label=t1)
    chart.add_series(x=df2.index, y=df2['y'], label=t2)
    chart.add_series(x=df3.index, y=df3['y'], label=t3)

    chart.add_horizontal_line()
    chart.add_last_value_badge(decimals=2)

    chart.legend(ncol=3)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
