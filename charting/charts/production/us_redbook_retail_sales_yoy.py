import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


DEFAULT_START_DATE = datetime.date(2013, 11, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    fred = FredSource()
    title = "Redbook Research: Same Store, Retails Sales Average YoY"

    d1, t1 = blp.get_series(series_id='REDSWYOY Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    d2, t2 = fred.get_series(series_id='JHDUSRGDPBR', observation_start=observation_start.strftime("%Y-%m-%d"),
                             observation_end=observation_end.strftime("%Y-%m-%d"))

    metadata = Metadata(title=title, region=Region.US, category=Category.CONSUMER)
    chart = Chart(title=title, metadata=metadata, filename="us_redbook_retail_sales_yoy.png")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", y_lim=(-15, 25))

    chart.add_series(x=d1.index, y=d1['y'], label=t1)
    chart.add_vertical_line(x=d2.index, y=d2["y"], label="US Recession")
    chart.add_horizontal_line()

    chart.legend()
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
