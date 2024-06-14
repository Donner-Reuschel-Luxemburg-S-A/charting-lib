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

    df1, t1 = blp.get_series(series_id='I02177EU Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field='BX219')
    df2, t2 = blp.get_series(series_id='I02177EU Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field='BX218')
    df3, t3 = blp.get_series(series_id='I09502EU Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field='BX219')
    df4, t4 = blp.get_series(series_id='I09502EU Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field='BX219')

    title = "Securitized & Agency 7-10Y Spread"
    metadata = Metadata(title=title, region=Region.EU, category=Category.RATES)

    chart = Chart(title=title, num_rows=2, metadata=metadata, filename="securitzed_spreads.png")

    chart.configure_y_axis(row_index=0, label="BPS")
    chart.configure_y_axis(row_index=1, label="BPS")
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.add_series(row_index=0, x=df1.index, y=df1['y'], label="Securitized Spread to Swap")
    chart.add_series(row_index=0, x=df3.index, y=df3['y'], label="Agency Spread to Swap")
    chart.add_series(row_index=1, x=df2.index, y=df2['y'], label="Securitized Spread to Treasury")
    chart.add_series(row_index=1, x=df4.index, y=df4['y'], label="Agency Spread to Treasury")

    chart.legend(ncol=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
