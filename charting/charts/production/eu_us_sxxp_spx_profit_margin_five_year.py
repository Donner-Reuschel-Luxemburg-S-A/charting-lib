import datetime

import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.avg import Avg


def main(**kwargs):
    blp = BloombergSource()

    start = datetime.datetime.today().date() - relativedelta(years=5)

    df1, t1 = blp.get_series(series_id='SXXP Index', field="RR836", observation_start=start.strftime("%Y%m%d"))
    df2, t2 = blp.get_series(series_id='SPX Index', field="RR836", observation_start=start.strftime("%Y%m%d"))

    title = "Stoxx Euro 600 & S&P 500 Profit Margin"

    metadata = Metadata(title=title, region=[Region.EU, Region.US], category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="eu_us_sxxp_spx_profit_margin_five_year.png")

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", minor_locator=MultipleLocator(0.5),
                           major_locator=MultipleLocator(1))

    minor_locator = mdates.MonthLocator(interval=3)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1, transformer=Avg(offset=DateOffset(months=1)))
    chart.add_series(x=df2.index, y=df2['y'], label=t2, transformer=Avg(offset=DateOffset(months=1)))

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
