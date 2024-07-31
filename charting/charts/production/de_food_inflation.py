import datetime

import matplotlib.dates as mdates
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata
from charting.transformer.lead import Lead

DEFAULT_START_DATE = datetime.date(1992, 3, 31)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    title = "German food inflation and price expectations of food manufacturers"

    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    d1, t1 = blp.get_series(series_id='GRCPH11Y Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    d2, t2 = blp.get_series(series_id='GMFDDSE3 Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))

    chart = Chart(title=title, metadata=metadata, num_y_axis=2, filename="german_food_inflation.jpeg")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.configure_y_axis(y_axis_index=0, label="PERCENTAGE POINTS", y_lim=(-5, 22.5))
    chart.configure_y_axis(y_axis_index=1, label="INDEX", y_lim=(-20, 90))

    chart.add_series(x=d2.index, y=d2['y'], label=t2, y_axis_index=1, transformer=Lead(offset=DateOffset(months=6)))
    chart.add_series(x=d1.index, y=d1['y'], label=t1, y_axis_index=0)

    chart.add_last_value_badge()

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
