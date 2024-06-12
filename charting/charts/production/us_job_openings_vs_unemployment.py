import datetime

import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


DEFAULT_START_DATE = datetime.date(2000, 12, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    fred = FredSource()
    d1, t1 = fred.get_series(series_id='JTSJOL', observation_start=observation_start.strftime("%Y-%m-%d"),
                           observation_end=observation_end.strftime("%Y-%m-%d"))
    d2, t2 = fred.get_series(series_id='UNRATE', observation_start=observation_start.strftime("%Y-%m-%d"),
                           observation_end=observation_end.strftime("%Y-%m-%d"))
    d3, t3 = fred.get_series(series_id='JHDUSRGDPBR', observation_start=observation_start.strftime("%Y-%m-%d"),
                           observation_end=observation_end.strftime("%Y-%m-%d"))

    title = "Job Openings (Total Nonfarm) vs. Unemployment Rate"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)
    chart = Chart(title=title, metadata=metadata, filename="us_job_openings_vs_unemployment.png", num_y_axis=2)

    chart.configure_y_axis(y_axis_index=0, label="Level in Thousands")
    chart.configure_y_axis(y_axis_index=1, label="Percentage Points")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=d1.index, y=d1['y'], label=t1, y_axis_index=0, invert=True)
    chart.add_series(x=d2.index, y=d2['y'], label=t2, y_axis_index=1)
    chart.add_vertical_line(x=d3.index, y=d3["y"], label="US Recession")

    chart.add_last_value_badge(decimals=2)
    chart.legend(ncol=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
