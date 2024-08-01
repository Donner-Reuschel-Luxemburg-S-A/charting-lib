import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.ytd import Ytd

DEFAULT_START_DATE = datetime.date(2024, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    df2, t2 = blp.get_series(series_id='sxxp Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field="px_close_1d")
    df3, t3 = blp.get_series(series_id='mcxp Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field="px_close_1d")
    df4, t4 = blp.get_series(series_id='scxp Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field="px_close_1d")

    title = "European Indices Performance"

    metadata = Metadata(title=title, category=Category.EQUITY, region=Region.EU)
    chart = Chart(title=title, filename="eu_indices_yield.jpeg", metadata=metadata)

    chart.configure_y_axis(label="PERCENTAGE POINTS")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=df2.index, y=df2['y'], label=t2, transformer=Ytd())
    chart.add_series(x=df3.index, y=df3['y'], label=t3, transformer=Ytd())
    chart.add_series(x=df4.index, y=df4['y'], label=t4, transformer=Ytd())

    chart.add_horizontal_line()
    chart.add_last_value_badge(decimals=2)

    chart.legend(ncol=3)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
