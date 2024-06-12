import datetime

import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata
from charting.transformer.lead import Lead
from charting.transformer.resample import Resample


DEFAULT_START_DATE = datetime.date(1995, 1, 31)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    df1, t1 = blp.get_series(series_id='SBOIPRIC Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))
    df2, t2 = blp.get_series(series_id='CLEVCPIA Index', observation_start=observation_start.strftime("%Y%m%d"),
                             observation_end=observation_end.strftime("%Y%m%d"))

    title = "NFIB Small Business Higher Prices & Nat'l Fed. of Ind. Business"
    metadata = Metadata(title=title, region=Region.US, category=[Category.INFLATION, Category.SURVEY])
    chart = Chart(title=title, metadata=metadata, num_y_axis=2, filename="us_nfib_cpi.png")

    chart.configure_y_axis(y_axis_index=0, label="EUR €", y_lim=(-35, 70))
    chart.configure_y_axis(y_axis_index=1, label="EUR €")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=df1.index, y=df1['y'], label=t1, y_axis_index=0, fill=True,
                     fill_threshold=-35, transformer=[Resample('M'), Lead(offset=DateOffset(months=10))])
    chart.add_series(x=df2.index, y=df2['y'], label=t2, y_axis_index=1, transformer=Resample('M'))

    chart.legend()

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
