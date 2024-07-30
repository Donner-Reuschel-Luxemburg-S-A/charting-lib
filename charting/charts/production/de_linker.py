import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(2024, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    df1, t1 = blp.get_series(series_id='BN8684431 Govt', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field='YLD_YTM_MID')

    df3, t3 = blp.get_series(series_id='EK1581793 Govt', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field='YLD_YTM_MID')

    df5, t5 = blp.get_series(series_id='EK7815401 Govt', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"), field='YLD_YTM_MID')

    title = "Germany Real Rates"
    metadata = Metadata(title=title, region=Region.DE, category=Category.RATES)
    chart = Chart(title=title, metadata=metadata, filename="de_real_rates.jpeg")

    chart.configure_y_axis(label="Percentage Points")
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=df1.index, y=df1['y'], label="Germany Real Rate 2033")
    chart.add_series(x=df3.index, y=df3['y'], label="Germany Real Rate 2030")
    chart.add_series(x=df5.index, y=df5['y'], label="Germany Real Rate 2026")
    chart.add_last_value_badge(decimals=2)

    chart.legend(ncol=3)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
