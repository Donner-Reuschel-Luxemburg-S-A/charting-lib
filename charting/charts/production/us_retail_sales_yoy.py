import datetime

import matplotlib.dates as mdates
from pandas import DateOffset
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from charting.transformer.avg import Avg
from charting.transformer.pct import Pct

DEFAULT_START_DATE = datetime.date(2020, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    fred = FredSource()
    title = "US retail sales: YoY change"

    d1, t1 = fred.get_series(series_id='RSAFS', observation_start=observation_start.strftime("%Y-%m-%d"),
                             observation_end=observation_end.strftime("%Y-%m-%d"))

    metadata = Metadata(title=title, region=Region.US, category=Category.CONSUMER)
    chart = Chart(title=title, metadata=metadata, filename="us_retail_sales_yoy.png")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", y_lim=(0, 35))

    chart.add_series(x=d1.index, y=d1['y'], label=t1, chart_type='bar', bar_bottom=0,
                     transformer=[Pct(periods=12), Avg(offset=DateOffset(months=3))])

    chart.legend()

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
