import datetime

import matplotlib.dates as mdates
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.lead import Lead

DEFAULT_START_DATE = datetime.date(2020, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    d1, t1 = blp.get_series(series_id='MUVIYOY Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    d2, t2 = blp.get_series(series_id='MUVIMOM Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    d3, t3 = blp.get_series(series_id='CPRTUCT% Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))

    title = "Manheim US Vehicle Inflation"
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)
    chart = Chart(title=title, metadata=metadata, filename="us_vehicle_inflation.png", num_y_axis=2)

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", y_lim=(-55, 55))
    chart.configure_y_axis(y_axis_index=1, label="Percentage Points", y_lim=(-15, 15))

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=d2.index, y=d2['y'], label="Manheim US Used Vehicle Value (MoM)", chart_type='bar', alpha=0.7,
                     y_axis_index=1, transformer=Lead(offset=DateOffset(months=2)))
    chart.add_series(x=d1.index, y=d1['y'], label="Manheim US Used Vehicle Value (YoY)",
                     transformer=Lead(offset=DateOffset(months=2)))
    chart.add_series(x=d3.index, y=d3['y'], label=t3)

    chart.add_horizontal_line()
    chart.add_last_value_badge()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
