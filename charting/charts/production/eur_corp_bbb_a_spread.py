import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(2014, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    df, t = blp.get_series(series_id='I02202EU Index', observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"), field='BX218')
    df2, t2 = blp.get_series(series_id='I02201EU Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field='BX218')

    title = 'EUR Corporate BBB - A Spread'
    t = 'Bloomberg EuroAgg Corporate Baa EUR'
    t2 = 'Bloomberg EuroAgg Corporate A EUR'
    metadata = Metadata(title=title, region=Region.EU, category=Category.CREDIT)

    chart = Chart(title=title, num_rows=2, metadata=metadata, filename="eur_corp_bbb_a_spread.jpeg")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(row_index=0, label='BPS Spread To TSY')
    chart.configure_y_axis(row_index=1, label='Spread Difference BPS')

    chart.add_series(x=df.index, y=df['y'], label=t)
    chart.add_series(x=df2.index, y=df2['y'], label=t2)
    chart.add_series(x=df.index, y=(df - df2)['y'], row_index=1, label=title)
    chart.add_last_value_badge(decimals=2)

    chart.legend()

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
