import datetime

import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.pct import Pct
from charting.transformer.resample import Resample

DEFAULT_START_DATE = datetime.date(2017, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    df1, t1 = blp.get_series(series_id='SPX Index', field="RR906",
                             observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))

    title = "Quarterly S&P 500 Earnings Per Share"

    metadata = Metadata(title=title, region=Region.US, category=Category.EQUITY)
    chart = Chart(title=title, filename="us_spx_profits_quarterly.png", metadata=metadata, num_y_axis=2)

    chart.configure_y_axis(y_axis_index=0, label="USD $")
    chart.configure_y_axis(y_axis_index=1, label="Percentage Points")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=df1.index, y=df1['y'], chart_type='bar', transformer=[Resample('Q'), Pct(periods=4)], label=t1,
                     y_axis_index=1)

    df1 = df1[
        df1.index >= datetime.datetime(observation_start.year + 1, observation_start.month, observation_start.day)]

    chart.add_series(x=df1.index, y=df1['y'], transformer=Resample('Q'), label=t1)
    chart.add_horizontal_line(y_axis_index=1)

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
