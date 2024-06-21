import datetime

import matplotlib.dates as mdates
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata

DEFAULT_START_DATE = datetime.date(2000, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    fred = FredSource()

    us, us_title = fred.get_series(series_id='CPIAUCSL', observation_start=observation_start.strftime("%Y-%m-%d"),
                                   observation_end=observation_end.strftime("%Y-%m-%d"))
    de, de_title = fred.get_series(series_id='DEUCPALTT01CTGYM',
                                   observation_start=observation_start.strftime("%Y-%m-%d"),
                                   observation_end=observation_end.strftime("%Y-%m-%d"))
    jp, jp_title = fred.get_series(series_id='JPNCPIALLMINMEI',
                                   observation_start=observation_start.strftime("%Y-%m-%d"),
                                   observation_end=observation_end.strftime("%Y-%m-%d"))
    uk, uk_title = fred.get_series(series_id='GBRCPALTT01CTGYM',
                                   observation_start=observation_start.strftime("%Y-%m-%d"),
                                   observation_end=observation_end.strftime("%Y-%m-%d"))
    ch, ch_title = fred.get_series(series_id='CPALTT01CNM659N',
                                   observation_start=observation_start.strftime("%Y-%m-%d"),
                                   observation_end=observation_end.strftime("%Y-%m-%d"))

    us = (us.pct_change(periods=12) * 100).shift(1)
    jp = (jp.pct_change(periods=12) * 100).shift(1)

    title = "Inflation Trend"
    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.INFLATION)
    chart = Chart(title=title, metadata=metadata, filename="global_inflation.png")

    chart.configure_y_axis(label="Percentage Points")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_horizontal_line(y_axis_index=0)

    chart.add_series(x=us.index, y=us['y'], label="U.S.")
    chart.add_series(x=de.index, y=de['y'], label="Germany")
    chart.add_series(x=jp.index, y=jp['y'], label="Japan")
    chart.add_series(x=uk.index, y=uk['y'], label="UK")
    chart.add_series(x=ch.index, y=ch['y'], label="China")

    chart.legend(ncol=4)
    chart.add_last_value_badge(decimals=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
