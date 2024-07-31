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

    credit_small_df, credit_small_title = blp.get_series(series_id="SLDETGTS Index",
                                                         observation_start=observation_start.strftime("%Y%m%d"),
                                                         observation_end=observation_end.strftime("%Y%m%d"))
    credit_large_df, credit_large_title = blp.get_series(series_id="SLDETIGT Index",
                                                         observation_start=observation_start.strftime("%Y%m%d"),
                                                         observation_end=observation_end.strftime("%Y%m%d"))
    credit_consumer_df, credit_consumer_title = blp.get_series(series_id="SDCLTGTC Index",
                                                               observation_start=observation_start.strftime("%Y%m%d"),
                                                               observation_end=observation_end.strftime("%Y%m%d"))

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR',
                                                observation_start=observation_start.strftime("%Y-%m-%d"),
                                                observation_end=observation_end.strftime("%Y-%m-%d"))

    title = "US % of Bank Tightening Credit Standards"
    metadata = Metadata(title=title, region=Region.US, category=Category.CREDIT)

    chart = Chart(title=title, metadata=metadata, filename="us_credit_standards.jpeg")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(label="PERCENTAGE POINTS")

    chart.add_series(credit_small_df.index, credit_small_df['y'], label=credit_small_title)
    chart.add_series(credit_large_df.index, credit_large_df['y'], label=credit_large_title)
    chart.add_series(credit_consumer_df.index, credit_consumer_df['y'], label=credit_consumer_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line()
    chart.add_last_value_badge(decimals=2)

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
