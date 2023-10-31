import matplotlib.dates as mdates
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main():
    blp = BloombergSource()
    fred = FredSource()
    title = "Redbook Research: Same Store, Retails Sales Average"

    d1, t1 = blp.get_series(series_id='REDSWYOY Index', observation_start="20131101")
    d2, t2 = fred.get_series(series_id='JHDUSRGDPBR')

    metadata = Metadata(title=title, region=Region.US, category=Category.CONSUMER)
    chart = Chart(title=title, metadata=metadata, filename="us_redbook_retail_sales_yoy.png")

    minor_locator = mdates.MonthLocator(interval=3)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)
    chart.configure_y_axis(y_axis_index=0, label="% YoY", y_lim=(-15, 25))

    chart.add_series(x=d1.index, y=d1['y'], label=t1)
    chart.add_vertical_line(x=d2.index, y=d2["y"], label="US Recession")
    chart.add_horizontal_line()

    chart.legend()
    chart.plot()


if __name__ == '__main__':
    main()

