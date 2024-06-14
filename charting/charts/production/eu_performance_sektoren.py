import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata

DEFAULT_START_DATE = datetime.date(2024, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    df1, t1 = blp.get_series(series_id='LEATTREU Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df2, t2 = blp.get_series(series_id='LEGVTREU Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df3, t3 = blp.get_series(series_id='LECPTREU Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df4, t4 = blp.get_series(series_id='I02003EU Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))


    df1['y'] = (df1['y'] / df1['y'].iloc[0]) * 100
    df2['y'] = (df2['y'] / df2['y'].iloc[0]) * 100
    df3['y'] = (df3['y'] / df3['y'].iloc[0]) * 100
    df4['y'] = (df4['y'] / df4['y'].iloc[0]) * 100

    title = "European Interest Rate Markets Sectors"
    metadata = Metadata(title=title, region=Region.EU, category=Category.RATES)

    chart = Chart(title=title, metadata=metadata, filename="eu_rates_sector_performance.png")

    chart.configure_y_axis(label="Index")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=df1.index, y=df1['y'], label=t1)
    chart.add_series(x=df2.index, y=df2['y'], label=t2)
    chart.add_series(x=df3.index, y=df3['y'], label=t3)
    chart.add_series(x=df4.index, y=df4['y'], label=t4)

    chart.legend(ncol=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
