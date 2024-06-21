import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(1990, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    hy_ytw_df, hy_ytw_title = blp.get_series(series_id="LP01TREU Index", field="YIELD_TO_WORST",
                                             observation_start=observation_start.strftime("%Y%m%d"),
                                             observation_end=observation_end.strftime("%Y%m%d"))
    hy_cpn_df, hy_cpn_title = blp.get_series(series_id="LP01TREU Index", field="CPN",
                                             observation_start=observation_start.strftime("%Y%m%d"),
                                             observation_end=observation_end.strftime("%Y%m%d"))

    title = "Euro HY Corporates Refinancing Costs"
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="eu_hy_yield_coupon.png")
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(label="Percentage Points")

    chart.add_series(hy_ytw_df.index, hy_ytw_df['y'] - hy_cpn_df['y'],
                     label="Euro HY Corporates: Yield to Worst minus Coupon")

    chart.add_last_value_badge(decimals=2)
    chart.add_horizontal_line()
    chart.legend()

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
