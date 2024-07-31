import datetime

import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.avg import Avg

DEFAULT_START_DATE = datetime.datetime.today() - relativedelta(years=5)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    df1, t1 = blp.get_series(series_id='MXEF Index', field="RR836",
                             observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))

    title = "MSCI Emerging Markets Profit Margin"

    metadata = Metadata(title=title, region=Region.EM, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="eu_mxef_profit_margin.jpeg")

    chart.configure_y_axis(label="PERCENTAGE POINTS")
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=df1.index, y=df1['y'], label=t1, transformer=Avg(offset=DateOffset(months=1)))
    chart.add_last_value_badge(decimals=2)

    chart.legend()
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
