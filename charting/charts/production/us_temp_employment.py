import datetime

import matplotlib.dates as mdates
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region

DEFAULT_START_DATE = datetime.date(1990, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    fred = FredSource()
    d1, t1 = fred.get_series(series_id='TEMPHELPS', observation_start=observation_start.strftime("%Y-%m-%d"),
                             observation_end=observation_end.strftime("%Y-%m-%d"))
    d2, t2 = fred.get_series(series_id='JHDUSRGDPBR', observation_start=observation_start.strftime("%Y-%m-%d"),
                             observation_end=observation_end.strftime("%Y-%m-%d"))

    title = "Temporary Employment"
    metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)
    chart = Chart(title=title, metadata=metadata, filename="us_temp_employment.png")

    chart.configure_y_axis(label="Thousand of Persons")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=d1.index, y=d1['y'], label=t1)
    chart.add_vertical_line(x=d2.index, y=d2["y"], label="US Recession")

    chart.legend(ncol=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
