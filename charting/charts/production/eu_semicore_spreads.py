import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(2020, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    df1, t1 = blp.get_series(series_id='.FRA10 G Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df2, t2 = blp.get_series(series_id='.BGGER10 G Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df3, t3 = blp.get_series(series_id='.FINLGER G Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df4, t4 = blp.get_series(series_id='.AUSTGER G Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))

    title = "EU Semi Core Spreads"
    metadata = Metadata(title=title, region=Region.EU, category=Category.RATES)
    chart = Chart(title=title, metadata=metadata, filename="eu_semicore_spreads.jpeg")

    chart.configure_y_axis(label="BPS")
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(row_index=0, x=df1.index, y=df1['y'] * 100, label="France")
    chart.add_series(row_index=0, x=df2.index, y=df2['y'] * 100, label="Belgium")
    chart.add_series(row_index=0, x=df3.index, y=df3['y'], label="Finland")
    chart.add_series(row_index=0, x=df4.index, y=df4['y'], label="Austria")
    # chart.add_last_value_badge(decimals=0)
    chart.add_last_value_badge(decimals=2)

    chart.legend(4)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
