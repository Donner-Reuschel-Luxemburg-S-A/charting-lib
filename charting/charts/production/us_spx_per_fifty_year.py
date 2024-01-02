import datetime

import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.avg import Avg


def main():
    blp = BloombergSource()

    start = datetime.datetime.today().date() - relativedelta(years=15)

    df2, t2 = blp.get_series(series_id='SPX Index', field="RR900", observation_start=start.strftime("%Y%m%d"))

    title = "S&P 500 Price-Earnings Ratio"

    metadata = Metadata(title=title, region=Region.US, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="us_spx_per_fifty_year.png")

    chart.configure_y_axis(y_axis_index=0, label="P/E", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(2))

    minor_locator = mdates.YearLocator(base=1)
    major_locator = mdates.YearLocator(base=3)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df2.index, y=df2['y'], label=t2, transformer=Avg(offset=DateOffset(months=1)))

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
