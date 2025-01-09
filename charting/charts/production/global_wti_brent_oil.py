import datetime

import matplotlib.dates as mdates
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(2021, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    fred = FredSource()
    d1, t1 = fred.get_series(series_id='DCOILWTICO', observation_start=observation_start.strftime("%Y-%m-%d"),
                             observation_end=observation_end.strftime("%Y-%m-%d"))
    d2, t2 = fred.get_series(series_id='DCOILBRENTEU', observation_start=observation_start.strftime("%Y-%m-%d"),
                                observation_end=observation_end.strftime("%Y-%m-%d"))

    t1 = "Crude Oil WTI"
    t2 = "Crude Oil Brent"

    title = 'WTI & Brent Oil'
    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.COMMODITY)
    chart = Chart(title=title, metadata=metadata, filename="global_wti_brent_oil", language=kwargs.get('language', 'en'))

    chart.configure_y_axis(label="USD $")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=d1.index, y=d1['y'], label=t1)
    chart.add_series(x=d2.index, y=d2['y'], label=t2)
    chart.add_last_value_badge(decimals=2)

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
