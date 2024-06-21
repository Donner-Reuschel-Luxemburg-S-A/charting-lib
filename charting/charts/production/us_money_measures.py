import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata

DEFAULT_START_DATE = datetime.date(1929, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    fred = FredSource()

    m2_df, m2_title = blp.get_series(series_id="M2% YOY Index", observation_start=observation_start.strftime("%Y%m%d"),
                                     observation_end=observation_end.strftime("%Y%m%d"))

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR',
                                                observation_start=observation_start.strftime("%Y-%m-%d"),
                                                observation_end=observation_end.strftime("%Y-%m-%d"))

    title = "US Money Supply M2 YoY"
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="us_money_measures_yoy.png")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(label="Percentage Points")

    chart.add_series(m2_df.index, m2_df['y'], label=m2_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line()
    chart.legend(ncol=1)
    chart.add_last_value_badge(decimals=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
