import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from charting.transformer.ytd import Ytd

DEFAULT_START_DATE = datetime.date(2024, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    df1, t1 = blp.get_series(series_id='SX5E Index', field="px_close_1d",
                             observation_start=observation_start.strftime('%Y%m%d'),
                             observation_end=observation_end.strftime('%Y%m%d'))
    df2, t2 = blp.get_series(series_id='SXXP Index', field="px_close_1d",
                             observation_start=observation_start.strftime('%Y%m%d'),
                             observation_end=observation_end.strftime('%Y%m%d'))
    df3, t3 = blp.get_series(series_id='DAX Index', field="px_close_1d",
                             observation_start=observation_start.strftime('%Y%m%d'),
                             observation_end=observation_end.strftime('%Y%m%d'))
    df4, t4 = blp.get_series(series_id='SPX Index', field="px_close_1d",
                             observation_start=observation_start.strftime('%Y%m%d'),
                             observation_end=observation_end.strftime('%Y%m%d'))
    df5, t5 = blp.get_series(series_id='MXEF Index', field="px_close_1d",
                             observation_start=observation_start.strftime('%Y%m%d'),
                             observation_end=observation_end.strftime('%Y%m%d'))

    title = "Euro Stoxx 50, Stoxx Euro 600, DAX, S&P 500, Emerging Markets Performance"

    metadata = Metadata(title=title, category=Category.EQUITY, region=Region.GLOBAL)
    chart = Chart(title=title, metadata=metadata, filename="global_indices_performance.png")

    chart.configure_y_axis(label="Percentage Points")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=df1.index, y=df1['y'], label=t1, transformer=Ytd())
    chart.add_series(x=df2.index, y=df2['y'], label=t2, transformer=Ytd())
    chart.add_series(x=df3.index, y=df3['y'], label=t3, transformer=Ytd())
    chart.add_series(x=df4.index, y=df4['y'], label=t4, transformer=Ytd())
    chart.add_series(x=df5.index, y=df5['y'], label=t5, transformer=Ytd())

    chart.add_horizontal_line()
    chart.add_last_value_badge(2)

    chart.legend(ncol=3)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
