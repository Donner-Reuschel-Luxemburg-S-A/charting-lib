import datetime

import matplotlib.dates as mdates
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.avg import Avg

DEFAULT_START_DATE = datetime.date(1980, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    fred = FredSource()
    df1, t1 = blp.get_series(series_id='INJCJC Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df2, t2 = blp.get_series(series_id='SBOIHIRE Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df3, t3 = fred.get_series(series_id='JHDUSRGDPBR', observation_start=observation_start.strftime("%Y-%m-%d"),
                              observation_end=observation_end.strftime("%Y-%m-%d"))

    title = "Small Business hiring plans point to higher jobless claims"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)

    chart = Chart(title=title, num_y_axis=2, metadata=metadata, filename="us_nfib_jobless_claims.jpeg")

    chart.configure_y_axis(y_axis_index=0, label="THOUSANDS", y_lim=(100, 800))
    chart.configure_y_axis(y_axis_index=1, label="PERCENTAGE POINTS", y_lim=(-20, 30), reverse_axis=True)

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=df1.index, y=df1['y'], label=t1, y_axis_index=0, transformer=Avg(offset=DateOffset(months=1)))
    chart.add_series(x=df2.index, y=df2['y'], label=t2, y_axis_index=1)
    chart.add_vertical_line(x=df3.index, y=df3["y"], label="US Recession")

    chart.legend(ncol=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
