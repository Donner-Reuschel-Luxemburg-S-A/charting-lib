import datetime

import matplotlib.dates as mdates
import pandas as pd
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(2020, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    df1, t1 = blp.get_series(series_id='.NLDE10B G Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field='PX_LAST')
    df2, t2 = blp.get_series(series_id='AS4641773 Corp', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field='YLD_YTM_MID')
    df3, t3 = blp.get_series(series_id='EC8300625 Govt', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field='YLD_YTM_MID')

    common_index = pd.DatetimeIndex(
        set(df2.index).intersection(set(df3.index)).intersection(set(df1.index))).sort_values()
    title = "EU Core Spreads"
    metadata = Metadata(title=title, region=Region.EU, category=Category.RATES)
    chart = Chart(title=title, metadata=metadata, filename="eu_core_spreads.jpeg")

    chart.configure_y_axis(label="BPS")
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(row_index=0, x=common_index, y=df1.loc[common_index, 'y'], label="Netherlands")
    chart.add_series(row_index=0, x=common_index, y=(df2.loc[common_index, 'y'] - df3.loc[common_index, 'y']) * 100,
                     label="KFW")
    chart.legend(4)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
