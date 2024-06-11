import datetime

import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main(**kwargs):
    blp = BloombergSource()

    start = datetime.datetime.today().date() - relativedelta(years=15)
    df1, t1 = blp.get_series(series_id='USGG10YR Index', observation_start=start.strftime("%Y%m%d"))
    df2, t2 = blp.get_series(series_id='SPX Index', field="RR907", observation_start=start.strftime("%Y%m%d"))
    df = df2 - df1

    title = "S&P Earning Yields minus U.S. Treasury 10-Year"

    metadata = Metadata(title=title, region=Region.US, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="us_spx_profit_minus_ten_year_profit.png")

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", minor_locator=MultipleLocator(0.5),
                           major_locator=MultipleLocator(1))

    minor_locator = mdates.MonthLocator(interval=3)
    major_locator = mdates.YearLocator(base=2)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df.index, y=df['y'], label="SPX Index Earning Yields - USGG10YR Index")
    chart.add_horizontal_line()

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
