import datetime

import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main(**kwargs):
    blp = BloombergSource()

    start = datetime.datetime.today().date() - relativedelta(years=10)

    df1, t1 = blp.get_series(series_id='LECPOAS Index', observation_start=start.strftime("%Y%m%d"))

    title = "EUR Investment Grade Corporate Bond Spreads"

    metadata = Metadata(title=title, region=Region.EU, category=Category.FI)
    chart = Chart(title=title, filename="eu_ig_credit_spread.png", metadata=metadata)

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", minor_locator=MultipleLocator(0.1),
                           major_locator=MultipleLocator(0.5))

    minor_locator = mdates.YearLocator(base=1)
    major_locator = mdates.YearLocator(base=1)
    major_formatter = mdates.DateFormatter("%y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)
    mean_val = [df1['y'].mean()] * len(df1.index)
    chart.add_series(x=df1.index, y=df1['y'], label=t1)
    chart.add_series(x=df1.index, y=mean_val, label="10Y Avg", linestyle="--")

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
