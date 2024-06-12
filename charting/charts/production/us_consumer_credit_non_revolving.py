import datetime

import matplotlib.dates as mdates
import pandas as pd
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.avg import Avg


DEFAULT_START_DATE = datetime.date(2007, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()
    d1, t1 = blp.get_series(series_id='CCOSNREV Index', observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))

    d1["mom_change"] = d1["y"].diff()
    title = "US Nonrevolving Consumer Credit - Change on Month"
    metadata = Metadata(title=title, region=Region.US, category=Category.CREDIT)

    chart = Chart(title=title, metadata=metadata, filename="us_consumer_credit_non_revolving.png")

    chart.configure_y_axis(y_axis_index=0, label="Billion USD $", y_lim=(-15, 30))

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=d1.index, y=d1["mom_change"], label=t1, chart_type="bar")
    chart.add_series(x=d1.index, y=d1["mom_change"], label=t1, transformer=Avg(offset=pd.DateOffset(months=6)))

    chart.add_last_value_badge()

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
