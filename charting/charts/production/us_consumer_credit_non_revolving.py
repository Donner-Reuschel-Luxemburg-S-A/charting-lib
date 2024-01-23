import matplotlib.dates as mdates
import pandas as pd
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.avg import Avg


def main():
    blp = BloombergSource()
    d1, t1 = blp.get_series(series_id='CCOSNREV Index', observation_start="20070101")
    d1["mom_change"] = d1["y"].diff()
    title = "US Nonrevolving Consumer Credit - Change on Month"
    metadata = Metadata(title=title, region=Region.US, category=Category.CREDIT)

    chart = Chart(title=title, metadata=metadata, filename="us_consumer_credit_non_revolving.png")

    chart.configure_y_axis(y_axis_index=0, label="Billion $", y_lim=(-15, 30), minor_locator=MultipleLocator(5),
                           major_locator=MultipleLocator(10))

    minor_locator = mdates.YearLocator(base=1)
    major_locator = mdates.YearLocator(base=2)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1["mom_change"], label=t1, chart_type="bar")
    chart.add_series(x=d1.index, y=d1["mom_change"], label=t1, transformer=Avg(offset=pd.DateOffset(months=6)))

    chart.add_last_value_badge()
    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
