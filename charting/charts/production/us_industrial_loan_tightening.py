import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata
from charting.transformer.center import Center


DEFAULT_START_DATE = datetime.date(1992, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    fred = FredSource()
    d1, t1 = fred.get_series(series_id='DRTSCILM', observation_start=observation_start.strftime("%Y-%m-%d"),
                           observation_end=observation_end.strftime("%Y-%m-%d"))
    d2, t2 = fred.get_series(series_id='JHDUSRGDPBR', observation_start=observation_start.strftime("%Y-%m-%d"),
                           observation_end=observation_end.strftime("%Y-%m-%d"))
    d3, t3 = blp.get_series(series_id='NAPMPMI Index', observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))

    title = "As industrial loan standards tighten, manufacturing contracts"
    metadata = Metadata(title=title, region=Region.US, category=Category.CREDIT)
    chart = Chart(title=title, num_y_axis=2, metadata=metadata, filename="us_industrial_loan_tightening.png")

    chart.configure_y_axis(y_axis_index=0, label="PMI Index", y_lim=(20, 65))
    chart.configure_y_axis(y_axis_index=1, label="Percentage Points", reverse_axis=True)

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=d1.index, y=d1['y'], label="Tightening standards for C&I loans", y_axis_index=1)
    chart.add_series(x=d3.index, y=d3['y'], label=t3, chart_type='bar', y_axis_index=0, bar_bottom=50,
                     transformer=Center(val=50), alpha=0.7)
    chart.add_vertical_line(x=d2.index, y=d2["y"], label="US Recession")
    chart.add_horizontal_line(y_axis_index=1)

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
