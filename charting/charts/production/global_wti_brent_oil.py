from matplotlib.ticker import MultipleLocator
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
import matplotlib.dates as mdates


def main():
    fred = FredSource()
    d1, t1 = fred.get_series(series_id='DCOILWTICO', observation_start="2020-01-01")
    d2, t2 = fred.get_series(series_id='DCOILBRENTEU', observation_start="2020-01-01")

    title = 'WTI & Brent Oil'
    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.COMMODITY)
    chart = Chart(title=title, metadata=metadata, filename="global_wti_brent_oil.png")

    chart.configure_y_axis(y_axis_index=0, label="USD", minor_locator=MultipleLocator(5))

    major_locator = mdates.MonthLocator(interval=6)
    minor_locator = mdates.MonthLocator(interval=3)

    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label=t1)
    chart.add_series(x=d2.index, y=d2['y'], label=t2)

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()