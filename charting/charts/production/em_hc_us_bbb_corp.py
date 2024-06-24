import datetime

import matplotlib.dates as mdates
import pandas as pd
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(2014, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    df, t = blp.get_series(series_id='LG20STAT Index', observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"), field='BX218')
    df2, t2 = blp.get_series(series_id='LCB1TRUU Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field='BX218')
    title = 'EM HC USD vs US Corporate BBB'
    t = 'Bloomberg EM Hard Currency Aggregate TR Index Value Unhedged USD'
    t2 = 'Bloomberg Baa Corporate Total Return Index Value Unhedged USD'

    metadata = Metadata(title=title, region=Region.EU, category=Category.CREDIT)
    common_index = pd.DatetimeIndex(set(df.index).intersection(set(df2.index))).sort_values()
    chart = Chart(title=title, num_rows=2, filename="em_hc_us_bbb_corp.jpeg", metadata=metadata)

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(row_index=0, label='Spread BPS vs Tsy')
    chart.configure_y_axis(row_index=1, label='Spread Difference BPS')

    chart.add_series(x=common_index, y=df.loc[common_index]['y'], label=t)
    chart.add_series(x=common_index, y=df2.loc[common_index]['y'], label=t2)
    chart.add_series(x=common_index, y=(df.loc[common_index] - df2.loc[common_index])['y'], row_index=1, label=title)
    chart.legend()

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
