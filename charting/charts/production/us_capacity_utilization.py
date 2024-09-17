import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(1992, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    fred = FredSource()

    start_time = "19290101"

    cap_df, cap_title = blp.get_series(series_id="CPTICHNG Index",
                                       observation_start=observation_start.strftime("%Y%m%d"),
                                       observation_end=observation_end.strftime("%Y%m%d"))

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR',
                                                observation_start=observation_start.strftime("%Y-%m-%d"),
                                                observation_end=observation_end.strftime("%Y-%m-%d"))

    title = "US Capacity Utilization"
    metadata = Metadata(title=title, region=Region.US, category=Category.ECONOMY)

    chart = Chart(title=title, metadata=metadata, filename="us_capacity_utilization", language=kwargs.get('language', 'en'))

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(label="PERCENTAGE POINTS")

    chart.add_series(cap_df.index, cap_df['y'], label=cap_title)
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_last_value_badge(decimals=2)

    chart.legend(ncol=1)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
