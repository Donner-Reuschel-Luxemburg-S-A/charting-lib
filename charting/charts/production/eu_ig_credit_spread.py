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

    df1, t1 = blp.get_series(series_id='LBEATREU Index', field='BX218',
                             observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))

    title = "EUR Investment Grade Corporate Bond Spreads"

    metadata = Metadata(title=title, region=Region.EU, category=Category.FI)
    chart = Chart(title=title, filename="eu_ig_credit_spread.jpeg", metadata=metadata)

    chart.configure_y_axis(label="BPS Spread to TSY")
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    mean_val = [df1['y'].mean()] * len(df1.index)
    chart.add_series(x=df1.index, y=df1['y'], label=t1)
    chart.add_series(x=df1.index, y=mean_val, label="10Y Avg", linestyle="--")
    chart.add_last_value_badge(decimals=2)

    chart.legend(ncol=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
