import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(2017, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    fred = FredSource()
    df1, t1 = fred.get_series(series_id='DGS5', observation_start=observation_start.strftime("%Y-%m-%d"),
                              observation_end=observation_end.strftime("%Y-%m-%d"))
    df2, t2 = fred.get_series(series_id='DGS30', observation_start=observation_start.strftime("%Y-%m-%d"),
                              observation_end=observation_end.strftime("%Y-%m-%d"))

    df = df2 - df1

    title = "U.S. Treasury Spread 30-5-Year"
    metadata = Metadata(title=title, region=Region.US, category=Category.RATES)
    chart = Chart(title=title, metadata=metadata, filename="us_treasury_spread_30y_5y.png")

    chart.configure_y_axis(label="BPS")
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_horizontal_line()
    chart.add_series(x=df.index, y=df['y'] * 100, label=title)
    chart.add_last_value_badge(decimals=2)

    chart.legend()
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
