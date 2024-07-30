import datetime

import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.datetime.today() - relativedelta(years=10)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    df1, t1 = blp.get_series(series_id='I02201EU Index', field='BX218', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df2, t2 = blp.get_series(series_id='I02202EU Index', field='BX218', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))

    title = "EUR Investment Grade Corporate Bond Spreads"
    metadata = Metadata(title=title, region=Region.DE, category=Category.RATES)
    chart = Chart(title=title, num_rows=2, metadata=metadata, filename="eu_ig_credit_spread.jpeg")

    chart.configure_y_axis(row_index=0, label="BPS")
    chart.configure_y_axis(row_index=1, label="BPS")
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    mean_val = [df1['y'].mean()] * len(df1.index)
    chart.add_series(row_index=0, x=df1.index, y=df1['y'], label="Corporate A")
    chart.add_series(row_index=0, x=df1.index, y=mean_val, label="Corporate A - 10Y Avg", linestyle="--")

    mean_val = [df2['y'].mean()] * len(df2.index)
    chart.add_series(row_index=1, x=df2.index, y=df2['y'], label="Corporate BBB")
    chart.add_series(row_index=1, x=df2.index, y=mean_val, label="Corporate BBB - 10Y Avg", linestyle="--")

    chart.add_last_value_badge(decimals=0)

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
