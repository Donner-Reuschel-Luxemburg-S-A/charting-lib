import datetime

import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.datetime.today() - relativedelta(years=15)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    start = datetime.datetime.today().date() - relativedelta(years=15)
    df1, t1 = blp.get_series(series_id='USGG10YR Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df2, t2 = blp.get_series(series_id='SPX Index', field="RR907",
                             observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df = df2 - df1

    title = "S&P Earning Yields minus U.S. Treasury 10-Year"

    metadata = Metadata(title=title, region=Region.US, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="us_spx_profit_minus_ten_year_profit.jpeg")

    chart.configure_y_axis(label="PERCENTAGE POINTS")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=df.index, y=df['y'], label="SPX Index Earning Yields - USGG10YR Index")
    chart.add_horizontal_line()
    chart.add_last_value_badge(decimals=2)

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
