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
    df, t = blp.get_series(series_id='.ITGER10 G Index', observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))
    df2, t2 = blp.get_series(series_id='I02561EU Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field='BX218')
    title = 'EUR Corporate BBB - BTP/Bund Spread'
    t = 'BTPS - Bund 10Y Spread'
    t2 = 'Bloomberg Pan-European Aggregate: Corporate Baa Total Return'

    metadata = Metadata(title=title, region=Region.EU, category=[Category.CREDIT, Category.RATES])
    common_index = pd.DatetimeIndex(set(df.index).intersection(set(df2.index))).sort_values()

    chart = Chart(title=title, num_rows=2, filename="eur_corp_bbb_btp_spread.jpeg", metadata=metadata)

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(row_index=0, label='BPS Spread To TSY')
    chart.configure_y_axis(row_index=1, label='Spread Difference BPS')

    chart.add_series(x=common_index, y=df.loc[common_index]['y'] * 100, label=t)
    chart.add_series(x=common_index, y=df2.loc[common_index]['y'], label=t2)
    chart.add_series(x=common_index, y=(df.loc[common_index] * 100 - df2.loc[common_index])['y'], row_index=1,
                     label=title)
    chart.add_last_value_badge(decimals=2)

    chart.add_horizontal_line(row_index=1, y_axis_index=0, y=0)
    chart.legend()

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
