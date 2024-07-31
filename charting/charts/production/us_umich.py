import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata

DEFAULT_START_DATE = datetime.date(1978, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    fred = FredSource()

    sentiment_df, sentiment_title = blp.get_series(series_id="CONSSENT Index",
                                                   observation_start=observation_start.strftime("%Y%m%d"),
                                                   observation_end=observation_end.strftime("%Y%m%d"))
    expectations_df, expectations_title = blp.get_series(series_id="CONSEXP Index",
                                                         observation_start=observation_start.strftime("%Y%m%d"),
                                                         observation_end=observation_end.strftime("%Y%m%d"))
    conditions_df, conditions_title = blp.get_series(series_id="CONSCURR Index",
                                                     observation_start=observation_start.strftime("%Y%m%d"),
                                                     observation_end=observation_end.strftime("%Y%m%d"))

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR',
                                                observation_start=observation_start.strftime("%Y-%m-%d"),
                                                observation_end=observation_end.strftime("%Y-%m-%d"))

    title = "US University Michigan Surveys"
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_umich_surveys.jpeg", metadata=metadata)
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(label="INDEX")

    chart.add_series(sentiment_df.index, sentiment_df['y'], label=sentiment_title)
    chart.add_series(expectations_df.index, expectations_df['y'], label=expectations_title)
    chart.add_series(conditions_df.index, conditions_df['y'], label=conditions_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line(y=100)
    chart.legend(ncol=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
