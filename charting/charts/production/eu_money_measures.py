import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region

DEFAULT_START_DATE = datetime.date(1999, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    m1_df, m1_title = blp.get_series(series_id="ECMAM1YY Index", observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    m2_df, m2_title = blp.get_series(series_id="ECMAM2YY Index", observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    m3_df, m3_title = blp.get_series(series_id="ECMAM3YY Index", observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))

    title = "EU Money Supply Measures YoY"
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="eu_money_measures_yoy.png")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(label="Percentage Points")

    chart.add_series(m1_df.index, m1_df['y'], label=m1_title)
    chart.add_series(m2_df.index, m2_df['y'], label=m2_title)
    chart.add_series(m3_df.index, m3_df['y'], label=m3_title)

    chart.add_horizontal_line()
    chart.legend(ncol=1)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
